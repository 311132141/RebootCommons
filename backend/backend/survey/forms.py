from django.forms import ModelForm

from .models import UserSurvey

class UserSurveyForm(ModelForm):
    class Meta:
        model = UserSurvey
        fields = '__all__'