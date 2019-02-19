from django.core.exceptions import PermissionDenied
from django.http import Http404

from videos.forms import VideoForm as Form
from videos.models import VideoModel as Model
from videos.views.base import BaseCreateView, BaseDetailView, BaseView, BaseListView

APP_NAME = 'videoplayer'
MODEL = Model
MODEL_FORM = Form
MODEL_DESCRIPTION = 'where videos are stored'

MODEL_NAME = MODEL._meta.verbose_name
MODEL_NAME_PLURAL = MODEL._meta.verbose_name_plural
TEMPLATE_PATH = '{0}'.format(MODEL_NAME.replace(' ', '_').lower())
MODELPAGE_BASE_URL_NAME = '{0}_{1}'.format(APP_NAME, MODEL_NAME.replace(' ', '_').lower())


class ModelPageMixin(object):
    breadcrumbs = [{'name': APP_NAME, 'url_name': ''},
                   {'name': MODEL_NAME_PLURAL, 'url_name': '{0}_list'.format(MODELPAGE_BASE_URL_NAME)}]
    model = MODEL
    model_description = MODEL_DESCRIPTION
    model_name = MODEL_NAME
    model_name_plural = MODEL_NAME_PLURAL
    section_name = APP_NAME


class VideoCreateView(ModelPageMixin, BaseCreateView):
    form_class = MODEL_FORM
    page_name = 'Create {0}'.format(MODEL_NAME)
    success_url_name = '{0}_create'.format(MODELPAGE_BASE_URL_NAME)
    template_name = '{0}_create_or_update.html'.format(TEMPLATE_PATH)

    def get_context_data(self, **kwargs):
        all_videos = Model.active_objects.all()

        context = {'all_videos': all_videos}
        context.update(kwargs)
        return super(VideoCreateView, self).get_context_data(**context)

    def form_valid(self, form):
        """
        Overriding the inbuild method to save the current user instance
        """
        current_instance = form.instance
        current_instance.uploaded_by = self.request.user
        return super(VideoCreateView, self).form_valid(form)


class VideoPlayView(ModelPageMixin, BaseDetailView):
    page_name = 'Watch {}'.format(MODEL_NAME)
    template_name = '{0}_detail.html'.format(TEMPLATE_PATH)

    def get_context_data(self, **kwargs):
        video_uid = self.kwargs.get('uid',None)
        current_user = self.request.user
        video = Model.active_objects.get(uid=video_uid) if video_uid else None

        if video:
            if (not video.public_access ) and (video.uploaded_by != current_user):
                # If private video, only the uploaded member can access it
                raise PermissionDenied()
            context = {'video': video}

        else:
            # Raise 404 not found
            raise Http404

        # increase the view of that video
        video.views += 1
        video.save()
        return super(VideoPlayView, self).get_context_data(**context)

class VideoDashboardView(ModelPageMixin, BaseListView):
    page_name = 'Watch {}'.format(MODEL_NAME)
    template_name = '{0}_dashboard.html'.format(TEMPLATE_PATH)
    paginate_by = 10
    context_object_name = 'all_videos'
    queryset = Model.active_objects.all()

