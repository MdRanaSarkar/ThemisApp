from django.urls import path
from AIPI_App.views import (HomeView, DashIndex,
                            Showvideo, AudioCreate,
                            GoogleTranslator)

urlpatterns = [
    path('',HomeView, name ='home'),
    path("dashboard/", DashIndex, name ='dashboard'),
    path('audio_extract/', Showvideo, name= 'ShowAudioVideoDetails'),
    path('video_to_audio_convert', AudioCreate, name = 'audio_create'),
    path('google_translate/', GoogleTranslator, name = 'ShowGoogleTranslate'),
    
]
    