# Custom imports
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import CreateView, DetailView, ListView, TemplateView


class LoginRequiredMixin(object):
    """
    Class based view for validating login
    """
    user = None
    allowed = {}

    @method_decorator(ensure_csrf_cookie)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Function to validate if the user that has requested is active or not
        """
        try:
            if request.user.active:
                self.user = request.user

            else:
                raise PermissionDenied()

        except:
            raise PermissionDenied()

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Function to pass the context data while rendering the page.
        Data like user and if the user is allowed to access the page
        is passed here
        """
        context = {}
        context['user'] = self.user
        context['allowed'] = self.allowed
        context.update(kwargs)
        return super(LoginRequiredMixin, self).get_context_data(**context)


class TemplateAuthenticatedMixin(LoginRequiredMixin):
    breadcrumbs = []
    page_name = ''
    section_name = ''

    def get_context_data(self, **kwargs):
        """
        Function to pass the context data while rendering the page.
        Data like page_name and section name is passed here.
        """
        context = super(TemplateAuthenticatedMixin, self).get_context_data(**kwargs)
        context['breadcrumbs'] = self.breadcrumbs
        context['page_name'] = self.page_name
        context['section_name'] = self.section_name
        return context


class CRUDMixin(TemplateAuthenticatedMixin):
    action = ''
    model_description = ''
    model_name = ''
    model_name_plural = ''
    model_urlname = ''
    model = None

    def get_context_data(self, **kwargs):
        context = super(CRUDMixin, self).get_context_data(**kwargs)
        context['action'] = self.action
        context['model_description'] = self.model_description
        context['model_name'] = self.model_name
        context['model_name_plural'] = self.model_name_plural
        context['model_urlname'] = self.model_name.replace(' ', '_').lower()
        return context


class ModelFormMixin():
    """
    Class based view for Model Forms.
    Where the success urls are set, which will redirect from
    a form page to the set success url.
    """
    action_verb = 'processed'
    success_url_name = ''
    main_field_name = 'name'

    def __init__(self, *args, **kwargs):
        result = super(ModelFormMixin, self).__init__(*args, **kwargs)
        self.set_success_url()
        return result

    def set_success_url(self):
        self.success_url = reverse(self.success_url_name)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ModelFormMixin, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['logged_user'] = self.user
        return form_kwargs


class BaseView(TemplateAuthenticatedMixin, TemplateView):
    pass


class BaseCRUDView(CRUDMixin, TemplateView):
    pass


class BaseListView(CRUDMixin, ListView):
    """
    Class based view for List View of a Model.
    This view is used to show the list of instances of a model
    """
    action = 'List'

    def get_queryset(self):
        self.queryset = self.model.active_objects.all()
        return super(BaseListView, self).get_queryset()


class BaseCreateView(ModelFormMixin, CRUDMixin, CreateView):
    """
    Class based view for Create View of a Model.
    This view is used to create an instance of model
    """
    action = 'Create'
    action_verb = 'created'


class BaseDetailView(CRUDMixin, DetailView):
    """
    Class based view for Detail View of a Model.
    This view is used to show the detail of a model instance.
    """
    action = 'Detail'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
