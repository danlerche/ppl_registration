from django.forms import ModelForm
from .models import User, Event, Registration

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
