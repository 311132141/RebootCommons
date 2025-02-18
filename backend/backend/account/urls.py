# This Python code snippet is defining URL patterns for a Django application. Here's a breakdown of
# what it is doing:
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('companies/', api.get_companies, name='get_companies'),
    path('companies/<uuid:company_id>/', api.get_company_users, name='get_company_users'),
    path('companies/<uuid:company_id>/explanation/', api.CompanyExplanationView.as_view(), name='company-explanation'),
    path('users/<uuid:user_id>/explanation/', api.UserExplanationView.as_view(), name='user-explanation'),
]