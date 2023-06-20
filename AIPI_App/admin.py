from django.contrib import admin

# Register your models here.
from AIPI_App.models import Video, SpeechAudioFile, NudityImage, WeaponsImage, WeaponsVideo

admin.site.register(Video)

admin.site.register(SpeechAudioFile)

admin.site.register(NudityImage)


admin.site.register(WeaponsImage)

admin.site.register(WeaponsVideo)