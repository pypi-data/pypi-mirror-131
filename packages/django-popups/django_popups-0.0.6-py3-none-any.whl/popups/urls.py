from django.urls import path
from . import views

from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

app_name = 'popups'

urlpatterns = [
    path('', views.index, name='test'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
