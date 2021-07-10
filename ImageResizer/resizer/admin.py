from .models import *
from django.contrib import admin

'''Models registered in admin site'''
admin.site.register(UploadedFiles)
admin.site.register(ThumbnailSize)
admin.site.register(Plan)
admin.site.register(ExpireLink)
admin.site.register(UserDetail)
