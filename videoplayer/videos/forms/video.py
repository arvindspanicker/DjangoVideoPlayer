# Custom imports
from accounts.forms.base import BaseLoggedForm
from videos.models import VideoModel


class VideoForm(BaseLoggedForm):

    class Meta:
        model = VideoModel
        fields = ['title','video_file','public_access']
