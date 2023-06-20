from django.urls import path
from AIPI_App.views import (HomeView, DashIndex,
                            Showvideo, AudioCreate,
                            GoogleTranslator,
                            TextToSpeech,ImageToText, 
                            SpeechToText,NudityCheckerImg,
                            WeaponsDetections, WeaponsDetectionsFromVideo,
                            WeaponsDetectionsLive, WeaponsDetectWithLiveCamera
                            )

urlpatterns = [
    path('',HomeView, name ='home'),
    path("dashboard/", DashIndex, name ='dashboard'),
    path('audio_extract/', Showvideo, name= 'ShowAudioVideoDetails'),
    path('video_to_audio_convert', AudioCreate, name = 'audio_create'),
    path('google_translate/', GoogleTranslator, name = 'ShowGoogleTranslate'),
    path('text2speech/', TextToSpeech, name = 'texttospeech'),
    path('img2text/', ImageToText, name = 'imagetotext'),
    path('speech2text/', SpeechToText, name = 'speechtotext'),
    path('nuditycheckimg/',NudityCheckerImg, name = 'nuditycheckfromimg'),
    path('weapons_detection_img/',WeaponsDetections, name = 'weaponsdetectionimg'),
    path('weapons_detection_video/',WeaponsDetectionsFromVideo, name = 'weaponsdetectionvideo'),
     path('weapons_detection_live/',WeaponsDetectionsLive, name = 'weaponsdetectionlive'),
   path('livecamera/',WeaponsDetectWithLiveCamera, name = 'livecamera'),
]
    