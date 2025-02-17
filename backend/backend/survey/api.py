from collections import defaultdict
import random

from django.db import models
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    SurveyType, CourseType, SurveyTypeQuestion, CourseTypeQuestion,
    UserSurveyResponse, Answer, Question
)
from .serializers import QuestionSerializer
from account.models import User, Company
from account.serializer import *

# =============================================================================
# Constants and Mappings
# =============================================================================

DEMOGRAPHIC_MAPPING = {
    "귀하의 연령": "age",
    "귀하의 성별": "gender",
    "귀하의 소득": "salary",
    "귀하의 최종 학력": "education",
    "귀하의 결혼 유무": "marital",
    "귀하의 직군": "job_field",
    "귀하의 근무 형태": "employment_type",
    "귀하의 직급": "position",
    "귀하가 재직중인 회사 근속 기간": "tenure"
}

# Categories used for growth and performance comparisons
CATEGORIES = ["entrepreneur", "org", "selflead", "ppc"]

# =============================================================================
# Helper Functions
# =============================================================================

def get_company_user_count(company):
    """
    Returns the number of users in a company.
    """
    return User.objects.filter(company=company).count()


def get_company_average_growth(company):
    """
    Calculates the average growth of all users in a company.
    """
    company_users = User.objects.filter(company=company)
    categories = get_company_categories(company)
    
    if not categories or not company_users.exists():
        return 0  # Return 0 if no categories or users exist
    
    growth_data = calculate_growth(company_users, "Company", categories)
    
    # Compute overall average growth
    total_growth = sum(growth_data.values())
    average_growth = total_growth / len(growth_data) if growth_data else 0
    
    return round(average_growth, 2)  # Round to 2 decimal places


def get_company_course_type(company):
    """
    Returns the course type name for a company.
    """
    return company.course_type.name if company.course_type else "정보 없음"

def get_korean_question(english_key):
    """
    Returns the corresponding Korean question text for a given English key.
    """
    for korean, english in DEMOGRAPHIC_MAPPING.items():
        if english == english_key:
            return korean
    return None


def prepare_chart_data(queryset, field_name, colour_palette):
    """
    Prepares chart data from a queryset.

    Args:
        queryset (QuerySet): QuerySet containing grouping and count data.
        field_name (str): The field name to extract for labels.
        colour_palette (list): List of colours to use for the chart.

    Returns:
        dict: Dictionary containing labels and datasets.
    """
    labels = [entry[field_name] for entry in queryset]
    data = [entry['count'] for entry in queryset]
    return {
        "labels": labels,
        "datasets": [
            {
                "data": data,
                "backgroundColor": colour_palette[: len(labels)],
            }
        ]
    }


def get_user_basic_info(user):
    """
    Extracts basic user information.

    Args:
        user (User): The user instance.

    Returns:
        dict: Dictionary with the user's name and email.
    """
    return {
        "name": user.name,
        "email": user.email,
    }


def get_selected_program(user):
    """
    Retrieves the selected programme (CourseType) associated with the user.
    Returns the programme name or '정보 없음' if not found.
    """
    course_type = CourseType.objects.filter(
        usersurveyresponse__user=user
    ).values_list("name", flat=True).first()
    return course_type if course_type else "정보 없음"


def get_demographic_data(user):
    """
    Retrieves a user's demographic data from survey answers.

    Returns:
        dict: Mapping of demographic fields to user responses.
    """
    demographic_questions = {
        "gender": "귀하의 성별은?",
        "age": "귀하의 연령은?",
        "marital_status": "귀하의 결혼 유무는?",
        "education": "귀하의 최종 학력은?",
        "experience": "귀하의 경력은?",
        "job": "귀하의 직군",
        "income": "귀하의 소득",
    }

    demographics = {}
    for key, question_text in demographic_questions.items():
        answer = Answer.objects.filter(
            response__user=user,
            question__text__icontains=question_text
        ).values_list("answer_text", flat=True).first()
        demographics[key] = answer if answer else "정보 없음"

    demographics["selected_program"] = get_selected_program(user)
    return demographics


def calculate_average_score(user, phase, category):
    """
    Calculates the average score for a given user, survey phase, and category.

    Args:
        user (User): The user instance.
        phase (str): "pre" or "post" survey phase.
        category (str): Category name (e.g. entrepreneur, org, etc.).

    Returns:
        float: The average score (or 0 if none).
    """
    questions = Question.objects.filter(category__icontains=category)
    answers = Answer.objects.filter(
        response__user=user, response__phase=phase, question__in=questions
    )
    avg_score = answers.aggregate(avg=Avg("answer_value"))["avg"] or 0
    return avg_score


def calculate_growth(users, user_type="Generic", categories=None):
    """
    Computes the average percentage increase in survey scores for given categories.

    Args:
        users (QuerySet): Users to calculate growth for.
        user_type (str): Debug label.
        categories (list): List of categories to filter by.

    Returns:
        dict: Growth percentages for each category.
    """
    responses = UserSurveyResponse.objects.filter(user__in=users)
    answers = Answer.objects.filter(response__in=responses)

    if categories is None:
        return {}

    growth_data = {}
    for category in categories:
        questions = Question.objects.filter(category__icontains=category)
        category_answers = answers.filter(question__in=questions)

        pre_avg = category_answers.filter(response__phase="pre").aggregate(Avg("answer_value"))["answer_value__avg"]
        post_avg = category_answers.filter(response__phase="post").aggregate(Avg("answer_value"))["answer_value__avg"]

        if pre_avg and post_avg and pre_avg > 0:
            growth_data[category] = ((post_avg - pre_avg) / pre_avg) * 100
        else:
            growth_data[category] = 0  # Default to 0% growth if no valid data

        print(f"{user_type} Growth for {category}: {growth_data[category]:.2f}% (Pre: {pre_avg}, Post: {post_avg})")

    return growth_data


def get_company_categories(company):
    """
    Returns the list of categories based on the company's selected CourseType.

    Args:
        company (Company): The company instance.

    Returns:
        list: A list of category strings related to the company's course type.
    """
    if not company.course_type:
        return []

    return get_categories_by_course_type(company.course_type.name, "기업용")


def get_categories_by_course_type(course_name, survey_type_name="개인용"):
    """
    Returns the list of categories based on the given CourseType name.

    Args:
        course_name (str): The name of the course type.

    Returns:
        list: A list of category strings related to the course type.
    """
    if (survey_type_name == "개인용"):
        course_category_map = {
            "비전하우스": ["ppc_resilience", "ppc_hope", "ppc_optimism", "ppc_efficacy"],
            "리더십과 혁신": ["selflead_constructive", "selflead_natural", "selflead_behavior"],
            "기업가정신과 혁신": ["entrepreneur_risk", "entrepreneur_proact", "entrepreneur_innov"]
        }
    else:
        course_category_map = {
            "기업가정신과 혁신": ["entrepreneur_risk", "entrepreneur_proact", "entrepreneur_innov"],
            "리더십과 혁신": ["org_normative", "org_continuance", "org_affective", "selflead_constructive", "selflead_natural", "selflead_behavior"],
            "비전하우스": ["ppc_resilience", "ppc_hope", "ppc_optimism", "ppc_efficacy"]
        }

    return course_category_map.get(course_name, [])

def calculate_lifestyle_performance_growth(users):
    """
    Computes overall performance growth based on lifestyle question ratings.

    Args:
        users (QuerySet): Users whose responses will be used for the calculation.

    Returns:
        list: Formatted data containing lifestyle question, rating, and performance growth.
    """
    lifestyle_questions = Question.objects.filter(category="lifestyle")
    if not lifestyle_questions.exists():
        return []

    responses = UserSurveyResponse.objects.filter(user__in=users)
    lifestyle_answers = Answer.objects.filter(response__in=responses, question__in=lifestyle_questions)

    rating_users_map = defaultdict(lambda: defaultdict(set))
    for ans in lifestyle_answers:
        user_id = ans.response.user.id
        question_text = ans.question.text
        try:
            rating = int(ans.answer_value)
        except (TypeError, ValueError):
            rating = None
        if rating and 1 <= rating <= 5:
            rating_users_map[question_text][rating].add(user_id)

    formatted_data = []
    for question, rating_map in rating_users_map.items():
        for rating, user_ids in rating_map.items():
            if not user_ids:
                continue
            user_responses = UserSurveyResponse.objects.filter(user_id__in=user_ids)
            all_answers = Answer.objects.filter(response__in=user_responses)
            pre_avg = all_answers.filter(response__phase="pre") \
                                 .aggregate(Avg("answer_value"))["answer_value__avg"] or 0
            post_avg = all_answers.filter(response__phase="post") \
                                  .aggregate(Avg("answer_value"))["answer_value__avg"] or 0
            percentage_growth = ((post_avg - pre_avg) / pre_avg) * 100 if pre_avg else 0

            formatted_data.append({
                "question": question,
                "rating": rating,
                "growth": percentage_growth
            })

    return formatted_data


# =============================================================================
# API Views
# =============================================================================

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

    Example:
    GET /survey-types/1/courses/
    [
      { "id": 10, "name": "비전하우스", "description": "... (개인용)" },
      { "id": 11, "name": "리더십과 혁신", "description": "... (개인용)" }
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
    """
    Handles retrieval and submission of survey responses for a specific
    SurveyType and CourseType combination.
    """

    def get(self, request, survey_type_id, course_type_id):
        """
        Returns the questions for a specific SurveyType and CourseType combination.
        If the user is authenticated and has already submitted a survey response,
        then questions with category "lifestyle" are filtered out.
        """
        try:
            survey_type = SurveyType.objects.get(pk=survey_type_id)
            course_type = CourseType.objects.get(pk=course_type_id, survey_type=survey_type)
        except SurveyType.DoesNotExist:
            return Response({"detail": "SurveyType not found."}, status=status.HTTP_404_NOT_FOUND)
        except CourseType.DoesNotExist:
            return Response({"detail": "CourseType not found for this SurveyType."}, status=status.HTTP_404_NOT_FOUND)

        # Get questions from both bridging tables.
        survey_type_questions = SurveyTypeQuestion.objects.filter(
            survey_type=survey_type
        ).select_related('question').order_by('order')
        course_type_questions = CourseTypeQuestion.objects.filter(
            course_type=course_type
        ).select_related('question').order_by('order')

        st_questions = [stq.question for stq in survey_type_questions]
        ct_questions = [ctq.question for ctq in course_type_questions]
        combined_questions = st_questions + ct_questions

        # If the user is authenticated and has any previous response,
        # filter out lifestyle questions.
        if request.user and request.user.is_authenticated:
            if UserSurveyResponse.objects.filter(
                user=request.user, survey_type=survey_type, course_type=course_type
            ).exists():
                combined_questions = [q for q in combined_questions if ((q.category != "lifestyle") and (q.category != "demographic"))]

        serializer = QuestionSerializer(combined_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, survey_type_id, course_type_id):
        """
        Handles submission of user responses for a specific SurveyType and CourseType combination.
        Determines the phase automatically:
          - If no pre-phase response exists, phase is set to "pre".
          - If a pre-phase exists but no post-phase exists, phase is set to "post"
            and answers for lifestyle questions are skipped.
          - If both pre and post responses exist, further submissions are rejected.
        """
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            survey_type = SurveyType.objects.get(pk=survey_type_id)
            course_type = CourseType.objects.get(pk=course_type_id, survey_type=survey_type)
        except SurveyType.DoesNotExist:
            return Response({"detail": "SurveyType not found."}, status=status.HTTP_404_NOT_FOUND)
        except CourseType.DoesNotExist:
            return Response({"detail": "CourseType not found for this SurveyType."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Determine phase automatically:
        pre_response = UserSurveyResponse.objects.filter(
            user=user, survey_type=survey_type, course_type=course_type, phase="pre"
        ).first()
        post_response = UserSurveyResponse.objects.filter(
            user=user, survey_type=survey_type, course_type=course_type, phase="post"
        ).first()

        if pre_response is None:
            phase = "pre"
        elif post_response is None:
            phase = "post"
        else:
            return Response(
                {"detail": "Both pre and post survey responses have already been submitted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        survey_response = UserSurveyResponse.objects.create(
            user=user,
            survey_type=survey_type,
            course_type=course_type,
            phase=phase
        )

        answers = request.data.get("answers", [])
        if not isinstance(answers, list):
            return Response({"detail": "Answers must be a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        for answer in answers:
            question_id = answer.get("question_id")
            answer_text = answer.get("answer_text")
            answer_value = answer.get("answer_value")

            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return Response(
                    {"detail": f"Question with id {question_id} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # For post-phase submissions, skip lifestyle questions.
            if phase == "post" and question.category == "lifestyle":
                continue

            Answer.objects.create(
                response=survey_response,
                question=question,
                answer_text=answer_text,
                answer_value=answer_value
            )

        return Response(
            {"detail": "Survey responses submitted successfully.", "phase": phase},
            status=status.HTTP_201_CREATED
        )

class GenderDistributionView(APIView):
    """
    Provides gender distribution data from surveys.
    """

    def get(self, request):
        data = (
            UserSurvey.objects.values('gender')
            .annotate(count=models.Count('gender'))
            .order_by('gender')
        )
        labels = [item['gender'] for item in data]
        values = [item['count'] for item in data]
        return Response({
            'labels': labels,
            'datasets': [
                {
                    'data': values,
                    'backgroundColor': ['#4F46E5', '#A78BFA'],
                }
            ]
        })


@api_view(['GET'])
def age_distribution(request):
    """
    Returns age distribution data from survey responses.
    """
    try:
        age_data = (
            UserSurvey.objects.values('age')
            .annotate(count=Count('age'))
        )
        colour_palette = ["#A78BFA", "#C4B5FD", "#DDD6FE", "#EDE9FE", "#F5F3FF"]
        chart_data = prepare_chart_data(age_data, 'age', colour_palette)
        return Response(chart_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gender_vs_leadership(request, company_id):
    """
    Fetches average leadership ratings split by gender.
    """
    try:
        print(f"Fetching gender vs leadership data for company ID: {company_id}")

        company = Company.objects.get(id=company_id)
        users = User.objects.filter(company=company)
        print(f"Company found: {company.name}, Total users: {users.count()}")

        responses = UserSurveyResponse.objects.filter(user__in=users)
        print(f"Total survey responses found: {responses.count()}")

        gender_question = Question.objects.filter(text__icontains="성별").first()
        if not gender_question:
            print("Error: Gender question not found.")
            return Response(
                {"error": "Gender question not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        print(f"Gender question ID: {gender_question.id}, Text: {gender_question.text}")

        leadership_questions = Question.objects.filter(category__icontains="selflead")
        print(f"Total leadership-related questions found: {leadership_questions.count()}")

        gender_answers = Answer.objects.filter(question=gender_question, response__in=responses)
        print(f"Total gender responses found: {gender_answers.count()}")

        user_genders = {ans.response.user.id: ans.answer_text for ans in gender_answers}
        print(f"User genders mapped: {len(user_genders)} users have gender recorded.")

        category_ratings = defaultdict(lambda: {"남성": [], "여성": []})
        for question in leadership_questions:
            answers = Answer.objects.filter(question=question, response__in=responses)
            print(f"Processing question ID: {question.id}, Category: {question.category}, Total answers: {answers.count()}")
            for ans in answers:
                user_id = ans.response.user.id
                gender = user_genders.get(user_id, "Unknown")
                if ans.answer_value is not None:
                    if gender in ["남성", "여성"]:
                        category_ratings[question.category][gender].append(ans.answer_value)

        formatted_data = []
        for category, ratings in category_ratings.items():
            male_avg = sum(ratings["남성"]) / len(ratings["남성"]) if ratings["남성"] else 0
            female_avg = sum(ratings["여성"]) / len(ratings["여성"]) if ratings["여성"] else 0
            print(f"Category: {category}, Male Avg: {male_avg}, Female Avg: {female_avg}")
            formatted_data.append({"category": category, "남성": male_avg, "여성": female_avg})

        print("Final computed data:", formatted_data)
        return Response({"data": formatted_data}, status=status.HTTP_200_OK)

    except Company.DoesNotExist:
        print(f"Error: Company with ID {company_id} not found.")
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_demographic_vs_survey_improvement(request, company_id, demographic_type):
    """
    Fetches average survey ratings split by a demographic type (age, salary, education, etc.),
    comparing pre vs post responses.

    Example URL: /api/companies/{company_id}/demographic-improvement/age/
    """
    try:
        print(f"Fetching {demographic_type} vs survey improvement data for company ID: {company_id}")

        korean_question_text = get_korean_question(demographic_type)
        if not korean_question_text:
            return Response({"error": "Invalid demographic category."}, status=status.HTTP_400_BAD_REQUEST)

        company = Company.objects.get(id=company_id)
        users = User.objects.filter(company=company)
        print(f"Company found: {company.name}, Total users: {users.count()}")

        question = Question.objects.filter(text__icontains=korean_question_text).first()
        if not question:
            return Response(
                {"error": f"Question not found for {demographic_type}."},
                status=status.HTTP_404_NOT_FOUND
            )
        print(f"Demographic question ID: {question.id}, Text: {question.text}")

        answers = Answer.objects.filter(question=question, response__user__in=users)
        print(f"Total {demographic_type} responses found: {answers.count()}")

        user_categories = {ans.response.user.id: ans.answer_text for ans in answers}
        survey_answers = Answer.objects.filter(response__user__in=users)
        print(f"Processing {survey_answers.count()} total answers.")

        category_ratings = defaultdict(lambda: {"pre": [], "post": []})
        for ans in survey_answers:
            user_id = ans.response.user.id
            category = user_categories.get(user_id, "Unknown")
            phase = ans.response.phase
            if ans.answer_value is not None:
                category_ratings[category][phase].append(ans.answer_value)

        formatted_data = []
        for category, phases in category_ratings.items():
            pre_avg = sum(phases["pre"]) / len(phases["pre"]) if phases["pre"] else 0
            post_avg = sum(phases["post"]) / len(phases["post"]) if phases["post"] else 0
            print(f"{demographic_type.capitalize()} Group: {category}, Pre Avg: {pre_avg}, Post Avg: {post_avg}")
            formatted_data.append({
                f"{demographic_type}_group": category,
                "pre": pre_avg,
                "post": post_avg
            })

        return Response({"data": formatted_data}, status=status.HTTP_200_OK)

    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_company_vs_industry_growth(request, company_id):
    """
    Computes the average percentage increase in survey scores for different categories.
    Returns growth for the company and the overall industry, based on its selected CourseType.
    """
    try:
        print(f"🔹 Fetching growth data for Company ID: {company_id}")

        # Get company and users
        company = Company.objects.get(id=company_id)
        company_users = User.objects.filter(company=company)
        all_users = User.objects.all()

        # Print debug info
        print(f"✅ Company: {company.name}")
        print(f"📌 Course Type: {company.course_type}")  # Debug course type
        print(f"👥 Company Users: {company_users.count()}, All Users: {all_users.count()}")

        # Get categories based on company's CourseType
        categories = get_company_categories(company)
        print(f"📊 Categories Used: {categories}")

        if not categories:
            print("❌ Error: Company has no valid course type.")
            return Response({"error": "Company has no valid course type."}, status=status.HTTP_400_BAD_REQUEST)

        # Compute growth
        company_growth = calculate_growth(company_users, "Company", categories)
        industry_growth = calculate_growth(all_users, "Industry", categories)

        response_data = {
            "categories": categories,
            "company_scores": [company_growth.get(cat, 0) for cat in categories],
            "industry_scores": [industry_growth.get(cat, 0) for cat in categories]
        }

        print("\n✅ Final Computed Growth Data:", response_data)
        return Response(response_data, status=status.HTTP_200_OK)

    except Company.DoesNotExist:
        print("❌ Error: Company not found.")
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET"])
@permission_classes([AllowAny])
def get_lifestyle_vs_performance_growth(request, company_id):
    """
    Computes overall performance growth based on lifestyle question ratings.
    Produces data for a heatmap where:
      - X-axis: Lifestyle-related questions.
      - Y-axis: Ratings (1-5).
      - Cell values: Percentage increase in overall performance for users who selected that rating.
      
    Output Format:
    {
        "data": [
            {
                "question": "나는 건강을 위해 운동한다.",
                "rating": 5,
                "growth": 18.75
            },
            ...
        ]
    }
    """
    try:
        company = Company.objects.get(id=company_id)
        users = User.objects.filter(company=company)

        formatted_data = calculate_lifestyle_performance_growth(users)
        if not formatted_data:
            return Response({"error": "No lifestyle questions found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"data": formatted_data}, status=status.HTTP_200_OK)

    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_profile(request, user_id):
    """
    Retrieves the user profile, combining basic information and demographic data.

    Output Format:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "demographics": {
            "gender": "남성",
            "age": "60대",
            "marital_status": "기혼",
            "education": "고등학교 졸업",
            "experience": "3-5년",
            "job": "영업",
            "income": "5000 이상",
            "selected_program": "리더십과 혁신"
        }
    }
    """
    try:
        user = User.objects.get(id=user_id)
        user_info = get_user_basic_info(user)
        demographics = get_demographic_data(user)
        return Response({**user_info, "demographics": demographics}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_user_pre_post_comparison(request, user_id):
    """
    Fetches a user's pre/post average scores for different categories based on their CourseType.

    Returns:
    {
        "categories": ["entrepreneur_risk", "entrepreneur_proact", "entrepreneur_innov"],
        "pre_scores": [value1, value2, value3],
        "post_scores": [value1, value2, value3]
    }
    """
    user = get_object_or_404(User, id=user_id)

    # Ensure user has a CourseType
    user_course_type = UserSurveyResponse.objects.filter(user=user).values_list("course_type__name", flat=True).first()
    if not user_course_type:
        return Response({"error": "User has no assigned course type."}, status=status.HTTP_400_BAD_REQUEST)

    # Get categories based on the user's CourseType
    categories = get_categories_by_course_type(user_course_type)
    if not categories:
        return Response({"error": "User's course type is unrecognized."}, status=status.HTTP_400_BAD_REQUEST)

    print(f"📌 User: {user.name}, Course Type: {user_course_type}")
    print(f"📊 Categories Used: {categories}\n")

    # Compute pre/post scores
    pre_scores = [calculate_average_score(user, "pre", category) for category in categories]
    post_scores = [calculate_average_score(user, "post", category) for category in categories]

    response_data = {
        "categories": categories,
        "pre_scores": pre_scores,
        "post_scores": post_scores
    }

    print("✅ Final Computed Pre/Post Comparison Data:", response_data)
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_vs_all_growth(request, user_id):
    """
    Compares a single user's growth versus the average growth of all users based on their course type.

    Returns:
    {
        "categories": ["entrepreneur_risk", "entrepreneur_proact", "entrepreneur_innov"],
        "user_scores": [value1, value2, value3],
        "all_users_scores": [value1, value2, value3]
    }
    """
    user = get_object_or_404(User, id=user_id)

    # Get the user's CourseType
    user_course_type = UserSurveyResponse.objects.filter(user=user).values_list("course_type__name", flat=True).first()
    if not user_course_type:
        return Response({"error": "User has no assigned course type."}, status=status.HTTP_400_BAD_REQUEST)

    # Get categories based on the user's CourseType
    categories = get_categories_by_course_type(user_course_type)
    if not categories:
        return Response({"error": "User's course type is unrecognized."}, status=status.HTTP_400_BAD_REQUEST)

    print(f"📌 User: {user.name}, Course Type: {user_course_type}")
    print(f"📊 Categories Used: {categories}")

    # Compute growth for the individual user and all users based on relevant categories
    user_growth = calculate_growth([user], "Individual User", categories)
    all_users = User.objects.all()
    all_users_growth = calculate_growth(all_users, "All Users", categories)

    response_data = {
        "categories": categories,
        "user_scores": [user_growth.get(cat, 0) for cat in categories],
        "all_users_scores": [all_users_growth.get(cat, 0) for cat in categories]
    }

    # print("✅ Final Computed User vs All Growth Data:", response_data)
    return Response(response_data, status=status.HTTP_200_OK)

    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_users_lifestyle_performance_growth(request):
    """
    Computes overall performance growth for lifestyle-related questions across ALL users.
    """
    users = User.objects.all()
    formatted_data = calculate_lifestyle_performance_growth(users)

    if not formatted_data:
        return Response({"error": "No lifestyle questions found."}, status=status.HTTP_404_NOT_FOUND)

    return Response({"data": formatted_data}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_user_question_pre_post_comparison(request, user_id):
    """
    Fetches a user's pre/post scores for each question within their CourseType categories.

    Returns:
    {
        "categories": [
            {
                "name": "entrepreneur_risk",
                "questions": [
                    { "question": "나는 새로운 아이디어를 시도하는 것이 중요하다고 생각한다.", "pre_score": 3.2, "post_score": 4.1 },
                    { "question": "위험을 감수하는 것이 내 경력에 중요하다.", "pre_score": 2.8, "post_score": 3.5 }
                ]
            },
            ...
        ]
    }
    """
    user = get_object_or_404(User, id=user_id)

    # Ensure user has a CourseType
    user_course_type = UserSurveyResponse.objects.filter(user=user).values_list("course_type__name", flat=True).first()
    if not user_course_type:
        return Response({"error": "User has no assigned course type."}, status=status.HTTP_400_BAD_REQUEST)

    # Get categories for the user's CourseType
    categories = get_categories_by_course_type(user_course_type)
    if not categories:
        return Response({"error": "User's course type is unrecognized."}, status=status.HTTP_400_BAD_REQUEST)

    print(f"📌 User: {user.name}, Course Type: {user_course_type}")
    print(f"📊 Categories Used: {categories}")

    # Fetch pre/post scores for each question within each category
    category_data = []
    for category in categories:
        questions = Question.objects.filter(category__icontains=category)
        question_data = []

        for question in questions:
            pre_score = Answer.objects.filter(
                response__user=user, response__phase="pre", question=question
            ).aggregate(Avg("answer_value"))["answer_value__avg"] or 0

            post_score = Answer.objects.filter(
                response__user=user, response__phase="post", question=question
            ).aggregate(Avg("answer_value"))["answer_value__avg"] or 0

            question_data.append({
                "question": question.text,
                "pre_score": pre_score,
                "post_score": post_score
            })

        category_data.append({
            "name": category,
            "questions": question_data
        })

    response_data = {
        "categories": category_data
    }

    print("✅ Final Computed Question-Level Pre/Post Data:", response_data)
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_company_statistics(request, company_id):
    """
    Returns company statistics, including:
    - Number of users
    - Average growth rate
    - Course type
    """
    try:
        company = Company.objects.get(id=company_id)

        data = {
            "user_count": get_company_user_count(company),
            "average_growth": get_company_average_growth(company),
            "course_type": get_company_course_type(company),
        }

        return Response(data, status=status.HTTP_200_OK)

    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_users_without_company(request):
    """
    Returns a list of all users who do not belong to any company (company=None)
    using the UserSerializer.
    """
    users = User.objects.filter(company__isnull=True)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# =============================================================================