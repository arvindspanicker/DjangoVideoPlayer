from django import forms


class BaseLoggedForm(forms.ModelForm):

    UNKNOWN_USERNAME = 'unknown'
    logged_user = None

    class Meta():
        pass

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user', None)
        super(BaseLoggedForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


