from django.db.models.query import QuerySet
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .services import create_tumbnail
from dateutil import parser
from .permissions import *
from rest_framework.permissions import IsAuthenticated


class Index(ViewSet):
    def list(self, request):
        url_list = request.build_absolute_uri(
            reverse('resizer:list-list'))
        url_upload = request.build_absolute_uri(
            reverse('resizer:upload-list'))
        return Response({
            'User images list': url_list,
            'Upload new image': url_upload
        })


class FileUploadView(ViewSet):
    '''View for image upload'''
    serializer_class = FileListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response("Upload your image")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        request.data.update({"user": str(request.user.id)})
        serializer = UploadedFileSerializer(
            data=request.data)
        if serializer.is_valid():
            new_file = serializer.save()
            create_tumbnail(name=file_uploaded.name,
                            location=serializer.data["file_uploaded"], user=request.user)
            return redirect('resizer:list-list',)
        return Response(serializer.errors)


class FileListView(ViewSet):
    '''View with users listed images/thumbnails'''
    permission_classes = [IsAuthenticated]
    serializer_class = UploadedFileSerializer

    def list(self, request):
        queryset = UserDetail.objects.get(
            user=request.user).plan.uploadedfiles_set.all()
        get_original_file = UploadedFiles.objects.filter(
            user=request.user, original=True)
        serializer = FileListSerializer(queryset, many=True, context={"request":
                                                                      request})
        originall_file_serializer = FileListSerializer(get_original_file, many=True, context={"request":
                                                                                              request})
        url = request.build_absolute_uri(reverse('resizer:expire-list'))
        users_plan = UserDetail.objects.get(user=request.user).plan
        return Response({'thumbnails': serializer.data,
                         'originally_uloaded_files': originall_file_serializer.data if users_plan.get_origial else "Please update your plan",
                         'expiring_link': url if users_plan.get_expiring_link else "Please update your plan"
                         })


class CreateExpiringLinkView(ViewSet):
    '''View for creating exipiring links'''
    permission_classes = [IsAuthenticated, HasExpireLinkCreateAccess]
    serializer_class = ExpireLinkSerializer

    def create(self, request):
        serializer = ExpireLinkSerializer(
            data=request.data, context={'request': request})
        sec = serializer.initial_data['delayed_time']
        if serializer.is_valid():
            saved_expiring_properties = serializer.save(generated=datetime.now(),
                                                        expire_time=datetime.now()+timedelta(seconds=int(sec)))
            return redirect('resizer:exlink-detail', saved_expiring_properties.id)
        return Response(serializer.errors)


class GetExpiringLinkView(ViewSet):
    '''View with expiring link data'''
    permission_classes = [IsAuthenticated,
                          HasExpireLinkCreateAccess, HasExpireLinkAccess]
    serializer_class = ExpireLinkSerializer

    def retrieve(self, request, pk):
        get_expiring_link_data = ExpireLink.objects.get(pk=pk)
        link_data_serializer = ExpireLinkSerializer(
            get_expiring_link_data, context={"request": request})

        link_expiration_date = parser.parse(
            link_data_serializer.data['expire_time'], ignoretz=True)
        if datetime.now() <= link_expiration_date:
            get_expiring_file = UploadedFiles.objects.get(
                pk=get_expiring_link_data.files_id)
            link_serializer = UploadedFileSerializer(
                get_expiring_file, context={"request": request})

        return Response({
            'data': link_data_serializer.data,
            'link': link_serializer.data if datetime.now() <= link_expiration_date else 'Expired',
        })
