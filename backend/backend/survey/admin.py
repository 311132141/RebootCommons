from django.contrib import admin
from .models import SurveyType, CourseType, Question, SurveyTypeQuestion, CourseTypeQuestion, UserSurveyResponse, Answer


@admin.register(SurveyType)
class SurveyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'survey_type', 'description')
    list_filter = ('survey_type',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type')
    search_fields = ('text',)
    list_filter = ('question_type',)

    # Customize the form display in the admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # If the question type is 'radio' or 'checkbox', make the options field required
        if obj and obj.question_type in ['radio', 'checkbox']:
            form.base_fields['options'].required = True
        else:
            form.base_fields['options'].required = False
        return form

    # Allow inline editing of options (useful for JSON fields)
    def render_change_form(self, request, context, *args, **kwargs):
        if context['adminform'].form.instance.question_type in ['radio', 'checkbox']:
            context['adminform'].form.fields['options'].help_text = "Provide options as a JSON array (e.g., [\"Option 1\", \"Option 2\"])."
        return super().render_change_form(request, context, *args, **kwargs)


# Register the Question model with the custom admin
admin.site.register(Question, QuestionAdmin)

@admin.register(SurveyTypeQuestion)
class SurveyTypeQuestionAdmin(admin.ModelAdmin):
    list_display = ('survey_type', 'question', 'order', 'is_required')
    list_filter = ('survey_type',)


@admin.register(CourseTypeQuestion)
class CourseTypeQuestionAdmin(admin.ModelAdmin):
    list_display = ('course_type', 'question', 'order', 'is_required')
    list_filter = ('course_type',)


@admin.register(UserSurveyResponse)
class UserSurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey_type', 'course_type', 'phase', 'created_at')
    list_filter = ('survey_type', 'course_type', 'phase')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'answer_text', 'answer_value')
    list_filter = ('response__survey_type', 'response__course_type')
