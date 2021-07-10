from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .views import FileUploadView

app_name = "resizer"

router = routers.SimpleRouter()
router.register(r'', Index, basename="index")
router.register(r'upload', FileUploadView, basename="upload")
router.register(r'list', FileListView, basename="list")
router.register(r'expire', CreateExpiringLinkView, basename="expire")
router.register(r'exlink', GetExpiringLinkView, basename="exlink")

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
