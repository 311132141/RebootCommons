from rest_framework import serializers
from .models import UserSurvey
from .survey_questions import SURVEY_QUESTIONS

class UserSurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    answers = serializers.JSONField(required=False)
    class Meta:
        model = UserSurvey
        fields = '__all__'
        # read_only_fields = ['user']
    
    def get_questions(self, obj):
        #Fetch the survey questions for the user's survey type
        questions = SURVEY_QUESTIONS.get('common', {}).get('questions', [])
        specific_questions = SURVEY_QUESTIONS.get(obj.survey_type, {}).get('questions', [])
        return questions + specific_questions
