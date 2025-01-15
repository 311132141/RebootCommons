from django.contrib import admin
from .models import UserSurvey


# @admin.register(UserSurvey)
# class UserSurveyAdmin(admin.ModelAdmin):
#     list_display = ['user', 'gender', 'age', 'marital_status', 'education']
#     list_filter = ['gender', 'marital_status', 'education']
#     search_fields = ['user__email', 'user__name']
admin.site.register(UserSurvey)