from PIL import Image
import os
from django.conf import settings
from .models import *
from datetime import datetime as dt


def create_tumbnail(user, location, name):
    '''Creates thumbnails from originally upload files based on users cuirrent Plan'''
    size = UserDetail.objects.get(user=user).plan.size.all()
    new_path = dt.strftime(dt.now(), "images/%Y%m%d")
    for s in size:
        image = Image.open(os.path.join(settings.BASE_DIR)+"/"+location)
        image.thumbnail((s.thumbnail_width, s.thumbnail_height))
        save_dir = (os.path.join(settings.BASE_DIR, 'media/', new_path,
                                 'thumbnail'+str(s.thumbnail_width)+'x'+str(s.thumbnail_height)+'_'+str(user)+'_'+str(name))).replace("\\", "/")
        image.save(save_dir)
        file_uploaded = (os.path.join(new_path,
                                      'thumbnail'+str(s.thumbnail_width)+'x'+str(s.thumbnail_height)+'_'+str(user)+'_'+str(name))).replace("\\", "/")
        newTnail = UploadedFiles.create_new_thumbnail(
            data={
                "user": user,
                "file_uploaded": file_uploaded,
                "original": False
            })

        UploadedFiles.add_plan_to_file(
            UserDetail.objects.get(user=user).plan, newTnail)
