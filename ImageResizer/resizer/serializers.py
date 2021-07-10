from rest_framework import serializers
from .models import *


class UploadedFileSerializer(serializers.ModelSerializer):
    '''UploadedFiles model serializer for saving data'''
    class Meta:
        model = UploadedFiles
        fields = ("file_uploaded",
                  "added",
                  "user")

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)


class FileListSerializer(serializers.ModelSerializer):
    '''UploadedFiles model serializer for UI forms'''
    class Meta:
        model = UploadedFiles
        fields = ("file_uploaded",
                  "added")

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)


class ExpireLinkSerializer(serializers.ModelSerializer):
    '''ExpireLink model serializer for getting data to create expiring link'''
    expire_time = serializers.DateTimeField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(ExpireLinkSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['files'].queryset = UploadedFiles.objects.filter(
            user=request_user)

    class Meta:
        model = ExpireLink
        fields = ("files",
                  "delayed_time",
                  "expire_time")
