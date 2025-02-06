# from django.urls import path
# from . import api
# from .api import SurveyView, GenderDistributionView, age_distribution
# # from .api import SurveyView

# urlpatterns = [
#     #path('survey/', api.survey_list, name='survey_list'),
#     # path('', SurveyView.as_view(), name='survey'),
#     # path('survey/create/', api.survey_create, name='survey_create'),
#     path('survey/<int:survey_type_id>/<int:course_type_id>/', api.SurveyView.as_view(), name='survey_view'),
#     path('graphs/gender-distribution/', GenderDistributionView.as_view(), name='gender-distribution'),
#     path('graphs/age-distribution/', age_distribution, name='age-distribution'),
# ]
from django.urls import path
from .api import (
    SurveyView, GenderDistributionView, age_distribution,
    SurveyTypeListView, CourseTypeListView
)

urlpatterns = [
    # 1) Returns a list of all SurveyTypes (개인용, 기업용, etc.)
    path('survey-types/', SurveyTypeListView.as_view(), name='survey_type_list'),

    # 2) Returns a list of CourseTypes for a given SurveyType ID
    path('survey-types/<int:survey_type_id>/courses/',
         CourseTypeListView.as_view(), name='course_type_courses'),

    # Existing endpoint: fetch or submit answers for given type & course
    path('survey/<int:survey_type_id>/<int:course_type_id>/',
         SurveyView.as_view(), name='survey_view'),

    # Graph endpoints
    path('graphs/gender-distribution/', GenderDistributionView.as_view(), name='gender-distribution'),
    path('graphs/age-distribution/', age_distribution, name='age-distribution'),
]

