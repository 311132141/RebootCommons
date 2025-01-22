from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSurveySerializer
from .models import UserSurvey
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .survey_questions import SURVEY_QUESTIONS
from django.db import models
from django.db.models import Count

CHOICE_MAPPING = {
    "gender": { "남성": "male", "여성": "female" },
    "age": { "20대": "20", "30대": "30", "40대": "40", "50대": "50", "60대": "60" },
    "marital_status": { "미혼": "single", "기혼": "married" },
    "education": {
        "고등학교 졸업": "highschool",
        "전문대 졸업": "diploma",
        "대학교 졸업": "bachelor",
        "석사 졸업": "master",
        "박사 졸업": "phd"
    },
    "position": { "사원": "staff", "주임": "junior", "대리": "assistant", "과장": "manager", "차장": "senior_manager", "부장": "director" }
}
# Create your views here.
@api_view(['GET'])
def survey_list(request):
    surveys = UserSurvey.objects.all()
    serializer = UserSurveySerializer(surveys, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def survey_create(request):
    serializer = UserSurveySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
    return JsonResponse(serializer.data, status=201)

class SurveyView(APIView):
    def get(self, request, survey_type=None):
        # Validate survey_type
        if survey_type not in SURVEY_QUESTIONS:
            return Response({"error": "Invalid survey type"}, status=400)

        # Fetch questions for the survey type
        questions = SURVEY_QUESTIONS['common']['questions'] + SURVEY_QUESTIONS[survey_type]['questions']
        return Response({"questions": questions})

    def post(self, request, survey_type=None):
        # Map display labels to valid choice values
        answers = request.data.get('answers', {})
        transformed_answers = {
            key: CHOICE_MAPPING[key].get(value, value)
            for key, value in answers.items()
            if key in CHOICE_MAPPING
        }

        # Add the raw `answers` field explicitly for storage
        transformed_answers['answers'] = answers

        # Add survey type for validation
        transformed_answers['survey_type'] = survey_type

        # Validate and save the transformed data
        serializer = UserSurveySerializer(data=transformed_answers)
        if serializer.is_valid():
            serializer.save(user=request.user if request.user.is_authenticated else None)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class GenderDistributionView(APIView):
    def get(self, request):
        # Query the database for gender counts
        data = (
            UserSurvey.objects.values('gender')
            .annotate(count=models.Count('gender'))
            .order_by('gender')
        )
        
        # Format the data for the frontend
        labels = [item['gender'] for item in data]
        values = [item['count'] for item in data]

        return Response({
            'labels': labels,  # ['Male', 'Female']
            'datasets': [
                {
                    'data': values,  # [count of Male, count of Female]
                    'backgroundColor': ['#4F46E5', '#A78BFA'],
                }
            ]
        })

# Utility function to prepare chart data
def prepare_chart_data(queryset, field_name, color_palette):
    labels = [entry[field_name] for entry in queryset]
    data = [entry['count'] for entry in queryset]
    return {
        "labels": labels,
        "datasets": [
            {
                "data": data,
                "backgroundColor": color_palette[: len(labels)],  # Match colors to the number of labels
            }
        ]
    }

@api_view(['GET'])
def age_distribution(request):
    try:
        # Query the database and group by the `age` field
        age_data = (
            UserSurvey.objects.values('age')
            .annotate(count=Count('age'))
        )

        # Use utility to prepare chart data
        color_palette = ["#A78BFA", "#C4B5FD", "#DDD6FE", "#EDE9FE", "#F5F3FF"]
        chart_data = prepare_chart_data(age_data, 'age', color_palette)

        return Response(chart_data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)