from django.urls import path
from . import api
# from .api import SurveyView

urlpatterns = [
    path('survey/', api.survey_list, name='survey_list'),
    # path('', SurveyView.as_view(), name='survey'),
    path('survey/create/', api.survey_create, name='survey_create'),
]
