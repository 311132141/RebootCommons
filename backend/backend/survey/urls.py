from django.urls import path
from . import api
from .api import SurveyView, GenderDistributionView, age_distribution
# from .api import SurveyView

urlpatterns = [
    path('survey/', api.survey_list, name='survey_list'),
    # path('', SurveyView.as_view(), name='survey'),
    path('survey/create/', api.survey_create, name='survey_create'),
    path('survey/<str:survey_type>/', SurveyView.as_view(), name='survey'),
    path('graphs/gender-distribution/', GenderDistributionView.as_view(), name='gender-distribution'),
    path('graphs/age-distribution/', age_distribution, name='age-distribution'),
]
