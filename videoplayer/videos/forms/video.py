from accounts.forms.base import BaseLoggedForm
from videoplayer.models import Video


class EventForm(BaseLoggedForm):

    class Meta:
        model = EventModel
        fields = ['notes', 'active']
