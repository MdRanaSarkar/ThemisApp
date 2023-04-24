from django.shortcuts import render
from .models import Video
from .forms import VideoForm
import moviepy.editor as mp
from django.http import HttpResponseRedirect, JsonResponse
from ThemisAppAIPI.settings import BASE_DIR
from os.path import join
# Create your views here.
from googletrans import Translator
import pyttsx3


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



