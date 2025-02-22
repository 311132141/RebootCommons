
from django.urls import path
from .api import *

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
    path("companies/<uuid:company_id>/gender-leadership/", get_gender_vs_leadership, name="gender-leadership"),
    # path("companies/<uuid:company_id>/age-improvement/", get_age_vs_survey_improvement, name="age-improvement"),
    path("dashboard/<uuid:company_id>/demographic-improvement/<str:demographic_type>/", get_demographic_vs_survey_improvement, name="demographic-improvement"),
    path("dashboard/<uuid:company_id>/growth-comparison/", get_company_vs_industry_growth, name="growth-comparison"),
    # Lifestyle vs Performance Growth Heatmap
    path(
        "dashboard/<uuid:company_id>/lifestyle-performance-growth/",
        get_lifestyle_vs_performance_growth,
        name="lifestyle-performance-growth",
    ),
    path("users/<uuid:user_id>/profile/", get_user_profile, name="user-profile"),
    path("users/<uuid:user_id>/pre-post-comparison/", get_user_pre_post_comparison, name="user-pre-post-comparison"),
    path("users/<uuid:user_id>/user-growth-comparison/", get_user_vs_all_growth, name="user-growth-comparison"),
    path(
    "dashboard/lifestyle-performance-growth/all/",
    get_all_users_lifestyle_performance_growth,
    name="all-users-lifestyle-performance-growth",),
    path("users/<uuid:user_id>/question-pre-post-comparison/", get_user_question_pre_post_comparison, name="user-question-pre-post-comparison"),
    path("companies/<uuid:company_id>/statistics/", get_company_statistics, name="company-statistics"),
    path("users/no-company/", get_users_without_company, name="users_without_company"),
    path("companies/<uuid:company_id>/gender-counts/", get_gender_counts, name="gender-counts"),
    path("companies/<uuid:company_id>/overall-growth/", CompanyOverallGrowthView.as_view(), name="company-overall-growth"),
    path('users/<uuid:user_id>/overall-growth/', UserOverallGrowthView.as_view(), name='user-overall-growth'),
]

