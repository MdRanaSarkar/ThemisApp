from django.contrib import admin
from AttorneysApp.models import AreaOfPractise, AttorneysProfile, AwardInformations
# Register your models here.



class AreaOfPractiseAdmin(admin.ModelAdmin):
    list_display = ['title','updated_at']
    list_filter = ['created_at']
    search_fields = ['title']
admin.site.register(AreaOfPractise, AreaOfPractiseAdmin)


class AwardInformationsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at']

admin.site.register(AwardInformations, AwardInformationsAdmin)


class AttorneysProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'admission', 'created_at']
    list_filter = ['created_at']

admin.site.register(AttorneysProfile, AttorneysProfileAdmin)