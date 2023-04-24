from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField 
from django.utils.safestring import mark_safe
# Create your models here.


class AreaOfPractise(models.Model):
    title = models.CharField(max_length=200)
    details = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class AwardInformations(models.Model):
    title = models.CharField(max_length=200)
    details = RichTextUploadingField(blank=True, null=True)
    awardimg = models.ImageField(blank=True, upload_to='attoneysaward/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class AttorneysProfile(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(blank=True, upload_to='attoneys/')
    associate_at = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    award = models.ForeignKey(AwardInformations, on_delete=models.CASCADE, blank=True,null=True)
    biography = RichTextUploadingField()
    practisearea = models.ForeignKey(AreaOfPractise, on_delete=models.CASCADE)
    primary_number = models.CharField(max_length= 200, blank=True, null=True)
    contact = RichTextUploadingField()
    universityattended = models.CharField(blank=True, max_length=15)
    lawscholattended = models.CharField(blank=True, max_length=15)
    yearoffirstadmission = models.CharField(blank=True, max_length=50)
    admission = models.CharField(blank=True, max_length=50)
    membership = models.CharField(blank=True, max_length=50)
    birthinformation = models.CharField(blank=True, max_length=10)
    isln = models.CharField(blank=True, max_length=5)
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def imageUrl(self):
        if self.image:
            return self.image.url
        else:
            return ""

    def image_tag(self):
        return mark_safe('<img src="{}" heights="50" width="50" />'.format(self.image.url))
    image_tag.short_description = 'Image'
