from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.
from embed_video.fields import EmbedVideoField

class Video(models.Model):
    name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)

class SpeechAudioFile(models.Model):
    name= models.CharField(max_length=500)
    audiofile= models.FileField(upload_to='audio/', null=True, verbose_name="")

    def __str__(self):
        return self.name



class NudityImage(models.Model):
    name= models.CharField(max_length=500)
    image= models.FileField(upload_to='nnimg/', null=True, verbose_name="")

    def __str__(self):
        return self.name


class WeaponsImage(models.Model):
    name= models.CharField(max_length=500)
    image= models.FileField(upload_to='weaponsimgs/', null=True, verbose_name="")

    def __str__(self):
        return self.name

    def img_url(self):
        if self.image:
            return self.image.url


class WeaponsVideo(models.Model):
    name= models.CharField(max_length=500)
    video= models.FileField(upload_to='videos_uploaded',null=True,
validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def img_url(self):
        if self.video:
            return self.video.url




        
class EmbededItem(models.Model):
    video = EmbedVideoField()  # same like models.URLField()