from django.shortcuts import render
from .models import Video, SpeechAudioFile
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
        files = request.C
        print(csrf_token, files)
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



