from django.urls import path
from .views import upload_image, result
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', upload_image, name='upload'),
    path('result/<int:pk>/', result, name='result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
