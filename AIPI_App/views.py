from django.shortcuts import render
from .models import Video, SpeechAudioFile, NudityImage, WeaponsImage, WeaponsVideo, EmbededItem
from .forms import VideoForm
import moviepy.editor as mp
from django.http import HttpResponseRedirect, JsonResponse
from ThemisAppAIPI.settings import BASE_DIR
from os.path import join
# Create your views here.
from googletrans import Translator
import pyttsx3
from django.core.files.storage import FileSystemStorage 
from django.middleware.csrf import get_token
from .speech2text import Speechaudio2Text
from .imgnudity  import nuditydetectionresult
import requests
import os
import json
from .weaponsdetectai import WeaponsDetectedImgStore, WeaponsDetectionFromImageAI, WeaponsDetectedVideoFunc
import cv2
from django.urls import  reverse
from .SCvideoStream import stream, weaponsStream
import subprocess


def HomeView(request):
    context = {}
    return render(request, 'ClientView/IndexPage.html', context)



def DashIndex(request):
    context = {}
    return render(request, 'Dashboard/MiddleSection.html', context)




def AudioExtract(request):
    context = {}
    return render(request, 'Dashboard/MiddleSection.html', context)




def Showvideo(request):

    lastvideo= Video.objects.last()

    videofile= lastvideo.videofile


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    
    context= {'videofile': videofile,
              'form': form
              }
    
    return render(request, 'Dashboard/AudioExtract.html', context)


def AudioCreate(request):
    videofile= request.GET.get("video_src")
    print(videofile)
    print("my video clip:", join(BASE_DIR,videofile))
    my_clip = mp.VideoFileClip(join(BASE_DIR,videofile))
    
    my_clip.audio.write_audiofile(r"sada_kala_result.mp3")
    data = {
        "create_audio":True
    }
    return JsonResponse(data)


def GoogleTranslator(request):
    if request.method == "POST":
        lang = request.POST.get("lang", None)
        txt = request.POST.get("txt", None)

        translator = Translator()
        tr = translator.translate(txt, dest=lang)
        return render(request, 'ClientView/Translator_Section.html', {"result":tr.text})
    return render(request, 'ClientView/Translator_Section.html')


def TextToSpeech(request):
    context = {}
    if request.method == "POST":
        userbtn = ""
        inputtext = request.POST.get("inputtextdata", None)
        speechgender = request.POST.get("Gender", None)
        actionwisedata = request.POST.get("actiondata", None)
        print(actionwisedata)
        # pyttsx3 start 
        engine = pyttsx3.init()
        # rate = engine.getProperty('rate')
        engine.setProperty('rate', 125) 
        # volume = engine.getProperty('volume')
        engine.setProperty('volume',1.0)

        voices = engine.getProperty('voices')
        
        engine.setProperty('voice', voices[int(speechgender)].id)
        
        if actionwisedata == "DownLoadNow":
            engine.save_to_file(inputtext, 'test.mp3')
            engine.runAndWait()
            engine.stop()
        elif actionwisedata == "ListenNow":
            engine.say(inputtext)
            engine.runAndWait()
        return render(request, 'AIBasedTemplates/TextToSpeechSection.html', context)
    return render(request, 'AIBasedTemplates/TextToSpeechSection.html', context)

def ImageToText(request):
    
    if request.method == 'POST':
        csrf_token = get_token(request)
        img_lst = request.FILES['images']
        context = { "csrf_token": csrf_token,}
        print(img_lst)
    else:
        print("Nothing")
        context = {}
    return render(request, 'AIBasedTemplates/ImgToTextSection.html', context)

def SpeechToText(request):
    context = {}
    if request.method == 'POST':
        speechaudio = request.FILES['speech2textfiles']
        speechaudiofile = SpeechAudioFile.objects.create(
            name = speechaudio.name, audiofile = speechaudio)
        audio_path= speechaudiofile.audiofile.path
        generated_text = Speechaudio2Text(audio_path)
        context = { "speechaudio": generated_text}
        return render(request, 'AIBasedTemplates/SpeechToTextSection.html', context)
    return render(request, 'AIBasedTemplates/SpeechToTextSection.html', context)

def NudityCheckerImg(request):
    if request.method == 'POST' and 'nudityimginput' in request.FILES:
        imgfile = request.FILES['nudityimginput']
        ndi = NudityImage(name = imgfile.name, image = imgfile )
        ndi.save()
        # fss = FileSystemStorage()
        # file = fss.save(imgfile.name, imgfile)
        # file_url = fss.url(file)
        ndishow = NudityImage.objects.last()
        img_url = ndishow.image.url
        params = {
        'models': 'nudity-2.0',
        'api_user': '708482299',
        'api_secret': 'WWGyXX67SuGr2qE8JMmm'
        }
        files = {'media': open(os.path.dirname(os.path.realpath(__file__)) +  img_url, 'rb')}
        # files = open(file_url)
        r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

        output = json.loads(r.text)
        # imgdetails = nuditydetectionresult(file_url)
        context = {'file_url': files,
                   'nudityimgdetails' : output, 
                   }
        print(context)
        return render(request, 'AIBasedTemplates/NudityCheckerFromImg.html', {})
        print(imgfile)
    context = {}
    return render(request, 'AIBasedTemplates/NudityCheckerFromImg.html', context)




def WeaponsDetections(request):
    context = {}
    if request.method == "GET":
        return render(request, 'AIBasedTemplates/WeaponsDetection.html', context)
    if request.method == 'POST':
        files = request.FILES.getlist('files[]', None)
        print(files)
        imageName = []
        for f in files:
            # fs = FileSystemStorage()
            # file = fs.save(f.name, f)
            # fileurl = fs.url(file)
            # print("Fileurl", fileurl)
            weapons = WeaponsImage(name = f.name, image = f)
            weapons.save()
            weapons_db = WeaponsImage.objects.last()
            weapon_img_url =  weapons_db.img_url()
            # print("BASE_DIR", BASE_DIR)
            # print("image url", weapon_img_url)
            WeaponsDetectedImgStore(weapon_img_url, f.name)
            imageName.append(f.name)
            # print(f.name)
            # handle_uploaded_file(f)
        return JsonResponse({'msg':'<div class="alert alert-success" role="alert">File successfully uploaded</div>', 'detectedImgName':imageName})
    else:
        return render(request, 'AIBasedTemplates/WeaponsDetection.html', context )

def handle_uploaded_file(f):  
    with open('/static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 


def WeaponsDetectionsFromVideo(request):
    context = {}
    if request.method == "GET":
        return render(request, 'AIBasedTemplates/WeaponsDetectionFromVideo.html', context)
    if request.method == 'POST':
        vf = request.FILES
        print(vf)
        videofile = request.FILES.get('files')
        print(videofile)
        weaponsvideo = WeaponsVideo(name = videofile.name, video = videofile)
        weaponsvideo.save()
        weapons_db = WeaponsVideo.objects.last()
        weapon_img_url =  weapons_db.img_url()
        # print("BASE_DIR", BASE_DIR)
        # print("image url", weapon_img_url)
        WeaponsDetectedVideoFunc(weapon_img_url)
        return JsonResponse({'msg':'<div class="alert alert-success" role="alert">File successfully uploaded</div>', 'detectedVideoName':videofile.name})
    else:
        return render(request, 'AIBasedTemplates/WeaponsDetectionFromVideo.html', context )



def WeaponsDetectionsLive(request):
    context = {}
    if request.method == "GET":
        return render(request, 'AIBasedTemplates/WeaponsDetectionLive.html', context)
    if request.method == 'POST':
        vf = request.FILES
        print(vf)
        videofile = request.FILES.get('files')
        print(videofile)
        weaponsvideo = WeaponsVideo(name = videofile.name, video = videofile)
        weaponsvideo.save()
        weapons_db = WeaponsVideo.objects.last()
        weapon_img_url =  weapons_db.img_url()
        # print("BASE_DIR", BASE_DIR)
        # print("image url", weapon_img_url)
        WeaponsDetectedVideoFunc(weapon_img_url)
        return JsonResponse({'msg':'<div class="alert alert-success" role="alert">File successfully uploaded</div>', 'detectedVideoName':videofile.name})
    else:
        return render(request, 'AIBasedTemplates/WeaponsDetectionLive.html', context )

def WeaponsDetectWtihLiveCamera(request):
    # videocap = cv2.VideoCapture(0)
    weaponsStream()
    return HttpResponseRedirect(reverse('weaponsdetectionlive'))


def WeaponsDetectWithEmbededVideos(request):
    weapons_videos = EmbededItem.objects.all()    
    context = { 'embededvideos':weapons_videos }
    print(context)
    return render(request, 'AIBasedTemplates/weapons_detect_with_embeded_.html', context)

def detect_weapons():
    uploaded_path = r"https://www.youtube.com/watch?v=Ewu8_yi4JNk"
    subprocess.run(['python', 'C:\\Users\\HSSL110\\Desktop\\WebApp\\AIWebProject\\yolov5\\detect.py', '--weights',
                                'C:\\Users\\HSSL110\\Desktop\\WebApp\\AIWebProject\\static\\weight\\best.pt', '--imgsz', '1024', '--project', 'media/detect', '--source', uploaded_path])
    return uploaded_path


def ConcealledWeaponsDetect(request):
    context = { }
    print(context)
    return render(request, 'AIBasedTemplates/ConcealedWeaponsDetect.html', context)
