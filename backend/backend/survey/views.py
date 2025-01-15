from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import UserSurvey
from .serializers import UserSurveySerializer

# Create your views here.
@api_view(['GET'])
def survey_list(request):
    surveys = UserSurvey.objects.all()
    serializer = UserSurveySerializer(surveys, many=True)
    return JsonResponse({'data': serializer.data})