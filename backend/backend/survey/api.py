from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import SurveyType, CourseType, SurveyTypeQuestion, CourseTypeQuestion
from .serializers import QuestionSerializer
from django.db import models
from django.db.models import Count
from rest_framework.permissions import AllowAny

class SurveyTypeListView(APIView):
    permission_classes = [AllowAny]
    """
    Returns all available SurveyTypes.
    Example response:
    [
      { "id": 1, "name": "개인용", "description": "Personal usage" },
      { "id": 2, "name": "기업용", "description": "Corporate usage" }
    ]
    """
    def get(self, request):
        survey_types = SurveyType.objects.all()
        data = [
            {
                "id": st.id,
                "name": st.name,
                "description": st.description
            }
            for st in survey_types
        ]
        return Response(data, status=status.HTTP_200_OK)


class CourseTypeListView(APIView):
    permission_classes = [AllowAny]
    """
    Returns all CourseTypes for a given SurveyType ID.
    e.g. GET /survey-types/1/courses/ -> 
    [
      { "id": 10, "name": "비전하우스", "description": "... (개인용)" },
      { "id": 11, "name": "리더십과 혁신", "description": "... (개인용)" },
    ]
    """
    def get(self, request, survey_type_id):
        try:
            survey_type = SurveyType.objects.get(pk=survey_type_id)
        except SurveyType.DoesNotExist:
            return Response(
                {"detail": "SurveyType not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        course_types = survey_type.course_types.all()
        data = [
            {
                "id": ct.id,
                "name": ct.name,
                "description": ct.description
            }
            for ct in course_types
        ]
        return Response(data, status=status.HTTP_200_OK)
class SurveyView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, survey_type_id, course_type_id):
        """
        Returns the questions for a specific SurveyType and CourseType combination.
        """

        try:
            survey_type = SurveyType.objects.get(pk=survey_type_id)
            course_type = CourseType.objects.get(pk=course_type_id, survey_type=survey_type)
        except SurveyType.DoesNotExist:
            return Response({"detail": "SurveyType not found."}, status=status.HTTP_404_NOT_FOUND)
        except CourseType.DoesNotExist:
            return Response({"detail": "CourseType not found for this SurveyType."}, status=status.HTTP_404_NOT_FOUND)

        # 1. Fetch all bridging rows for the SurveyType, ordered by 'order'
        survey_type_questions = SurveyTypeQuestion.objects.filter(
            survey_type=survey_type
        ).select_related('question').order_by('order')

        # 2. Fetch all bridging rows for the CourseType, ordered by 'order'
        course_type_questions = CourseTypeQuestion.objects.filter(
            course_type=course_type
        ).select_related('question').order_by('order')

        # 3. Extract the actual Question objects from bridging
        #    (Or you can keep them separate if that suits your flow better)
        st_questions = [stq.question for stq in survey_type_questions]
        ct_questions = [ctq.question for ctq in course_type_questions]

        # Example: Combine them into a single list (e.g., first the SurveyTypeQuestions, then the CourseTypeQuestions)
        # If you want them strictly separated in different sections, keep them separate.
        combined_questions = st_questions + ct_questions

        # 4. Serialize the question objects
        serializer = QuestionSerializer(combined_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, survey_type_id, course_type_id):
        """
        Handles submission of user responses for a specific SurveyType and CourseType combination.
        """
        try:
            survey_type = SurveyType.objects.get(pk=survey_type_id)
            course_type = CourseType.objects.get(pk=course_type_id, survey_type=survey_type)
        except SurveyType.DoesNotExist:
            return Response({"detail": "SurveyType not found."}, status=status.HTTP_404_NOT_FOUND)
        except CourseType.DoesNotExist:
            return Response({"detail": "CourseType not found for this SurveyType."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the user
        user = request.user

        # Get the phase (pre/post) from the request body
        phase = request.data.get("phase")
        if phase not in ['pre', 'post']:
            return Response({"detail": "Invalid phase. Must be 'pre' or 'post'."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new UserSurveyResponse
        survey_response = UserSurveyResponse.objects.create(
            user=user,
            survey_type=survey_type,
            course_type=course_type,
            phase=phase
        )

        # Get the answers from the request body
        answers = request.data.get("answers", [])
        if not isinstance(answers, list):
            return Response({"detail": "Answers must be a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and create answers
        for answer in answers:
            question_id = answer.get("question_id")
            answer_text = answer.get("answer_text")
            answer_value = answer.get("answer_value")

            # Ensure the question exists and is part of the survey
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return Response({"detail": f"Question with id {question_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            # Create the Answer object
            Answer.objects.create(
                survey_response=survey_response,
                question=question,
                answer_text=answer_text,
                answer_value=answer_value
            )

        return Response({"detail": "Survey responses submitted successfully."}, status=status.HTTP_201_CREATED)

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