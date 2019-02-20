# Django Imports
from django.urls import path, re_path

# Custom Imports
from videos.views import VideoUploadView, VideoPlayView, VideoDashboardView

urlpatterns = [
    path('', VideoDashboardView.as_view(), {}, name='videoplayer_video_dashboard'),
    path('upload', VideoUploadView.as_view(), {}, name='videoplayer_video_create'),
    re_path('watch_video/(?P<uid>[^/]+)', VideoPlayView.as_view(), {}, name='videoplayer_play_create'),
]
