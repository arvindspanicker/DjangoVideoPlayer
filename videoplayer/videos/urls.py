from videos.views import VideoCreateView, VideoPlayView, VideoDashboardView
from django.urls import path, re_path

urlpatterns = [
    path('', VideoDashboardView.as_view(), {}, name='videoplayer_video_dashboard'),
    path('upload', VideoCreateView.as_view(), {}, name='videoplayer_video_create'),
    re_path('watch_video/(?P<uid>[^/]+)', VideoPlayView.as_view(), {}, name='videoplayer_play_create'),
]
