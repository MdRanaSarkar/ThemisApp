from django.contrib import admin

# Register your models here.
from AIPI_App.models import Video, SpeechAudioFile

admin.site.register(Video)

admin.site.register(SpeechAudioFile)