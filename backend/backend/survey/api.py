from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSurveySerializer
from .models import UserSurvey
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

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
# class SurveyView(APIView):
#     permission_classes = [AllowAny]  # Allow all users, including unauthenticated ones

#     def get(self, request):
#         # If the user is authenticated, fetch their survey
#         if request.user.is_authenticated:
#             try:
#                 survey = UserSurvey.objects.get(user=request.user)
#                 serializer = UserSurveySerializer(survey)
#                 return Response({"data": serializer.data}, status=200)
#             except UserSurvey.DoesNotExist:
#                 return Response({"message": "Survey not found"}, status=404)
#         else:
#             # For unauthenticated users, return a placeholder response or default data
#             return Response({"message": "No survey available for unauthenticated users"}, status=200)

#     def post(self, request):
#         # If the user is authenticated, associate the survey with their user
#         if request.user.is_authenticated:
#             survey, created = UserSurvey.objects.get_or_create(
#                 user=request.user,
#                 defaults={
#                     "age": 0,
#                     "gender": "",
#                     "marital_status": "",
#                     "education": "",
#                 },
#             )
#             serializer = UserSurveySerializer(instance=survey, data=request.data)
#         else:
#             # For unauthenticated users, create a survey without a user
#             serializer = UserSurveySerializer(data=request.data)

#         # Validate and save the survey data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "message": "Survey saved successfully",
#                     "data": serializer.data,
#                 },
#                 status=201,
#             )
#         return Response({"message": "Error", "errors": serializer.errors}, status=400)
