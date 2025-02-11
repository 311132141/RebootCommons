from rest_framework.views import APIView
from rest_framework.decorators import permission_classes

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import SurveyType, CourseType, SurveyTypeQuestion, CourseTypeQuestion, UserSurveyResponse, Answer, Question
from .serializers import QuestionSerializer
from django.db import models
from django.db.models import Count
from rest_framework.permissions import AllowAny
from django.db.models import Avg
from collections import defaultdict
from account.models import User, Company

# Korean to English Mapping for Demographic Questions
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

def get_korean_question(english_key):
    """
    Returns the corresponding Korean question text for a given English key.
    """
    for korean, english in DEMOGRAPHIC_MAPPING.items():
        if english == english_key:
            return korean
    return None

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
    # permission_classes = [AllowAny]
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
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
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
        # user = request.user
        user = request.user if request.user.is_authenticated else None

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
                response=survey_response,
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
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_gender_vs_leadership(request, company_id):
    """Fetches average leadership ratings split by gender."""

    try:
        print(f"Fetching gender vs leadership data for company ID: {company_id}")

        # Fetch company and users
        company = Company.objects.get(id=company_id)
        users = User.objects.filter(company=company)
        print(f"Company found: {company.name}, Total users: {users.count()}")

        # Get all survey responses from users in this company
        responses = UserSurveyResponse.objects.filter(user__in=users)
        print(f"Total survey responses found: {responses.count()}")

        # Identify gender question ID
        gender_question = Question.objects.filter(text__icontains="성별").first()
        if not gender_question:
            print("Error: Gender question not found.")
            return Response({"error": "Gender question not found."}, status=404)

        print(f"Gender question ID: {gender_question.id}, Text: {gender_question.text}")

        # Get all leadership-related questions
        leadership_questions = Question.objects.filter(category__icontains="selflead")
        print(f"Total leadership-related questions found: {leadership_questions.count()}")

        # Get gender answers for users in this company
        gender_answers = Answer.objects.filter(question=gender_question, response__in=responses)
        print(f"Total gender responses found: {gender_answers.count()}")

        # Map user ID to their gender
        user_genders = {ans.response.user.id: ans.answer_text for ans in gender_answers}
        print(f"User genders mapped: {len(user_genders)} users have gender recorded.")

        # Initialize data structure
        category_ratings = defaultdict(lambda: {"남성": [], "여성": []})

        # Process leadership answers
        for question in leadership_questions:
            answers = Answer.objects.filter(question=question, response__in=responses)
            print(f"Processing question ID: {question.id}, Category: {question.category}, Total answers: {answers.count()}")

            for ans in answers:
                user_id = ans.response.user.id
                gender = user_genders.get(user_id, "Unknown")  # Default to "Unknown" if no gender answer
                if ans.answer_value is not None:  # Ensure answer has a rating
                    if gender in ["남성", "여성"]:  # Only count known genders
                        category_ratings[question.category][gender].append(ans.answer_value)

        # Compute average ratings
        formatted_data = []
        for category, ratings in category_ratings.items():
            male_avg = sum(ratings["남성"]) / len(ratings["남성"]) if ratings["남성"] else 0
            female_avg = sum(ratings["여성"]) / len(ratings["여성"]) if ratings["여성"] else 0
            print(f"Category: {category}, Male Avg: {male_avg}, Female Avg: {female_avg}")
            formatted_data.append({"category": category, "남성": male_avg, "여성": female_avg})

        print("Final computed data:", formatted_data)
        return Response({"data": formatted_data}, status=200)

    except Company.DoesNotExist:
        print(f"Error: Company with ID {company_id} not found.")
        return Response({"error": "Company not found"}, status=404)
    
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def get_age_vs_survey_improvement(request, company_id):
#     """Fetches average survey ratings split by age group, comparing pre vs post responses."""

#     try:
#         print(f"Fetching age vs survey improvement data for company ID: {company_id}")

#         # Fetch company and users
#         company = Company.objects.get(id=company_id)
#         users = User.objects.filter(company=company)
#         print(f"Company found: {company.name}, Total users: {users.count()}")

#         # Get all survey responses from users in this company
#         responses = UserSurveyResponse.objects.filter(user__in=users)
#         print(f"Total survey responses found: {responses.count()}")

#         # Identify age question
#         age_question = Question.objects.filter(text__icontains="연령").first()
#         if not age_question:
#             print("Error: Age question not found.")
#             return Response({"error": "Age question not found."}, status=404)

#         print(f"Age question ID: {age_question.id}, Text: {age_question.text}")

#         # Get age answers for users in this company
#         age_answers = Answer.objects.filter(question=age_question, response__in=responses)
#         print(f"Total age responses found: {age_answers.count()}")

#         # Map user ID to their age group
#         user_ages = {ans.response.user.id: ans.answer_text for ans in age_answers}
#         print(f"User ages mapped: {len(user_ages)} users have age recorded.")

#         # Initialize data structure
#         age_ratings = defaultdict(lambda: {"pre": [], "post": []})

#         # Process all answers (no filtering)
#         answers = Answer.objects.filter(response__in=responses)
#         print(f"Processing {answers.count()} total answers.")

#         for ans in answers:
#             user_id = ans.response.user.id
#             age_group = user_ages.get(user_id, "Unknown")  # Default to "Unknown" if no age answer
#             phase = ans.response.phase  # 'pre' or 'post'

#             if ans.answer_value is not None and age_group in ["20대", "30대", "40대", "50대", "60대"]:  
#                 age_ratings[age_group][phase].append(ans.answer_value)

#         # Compute average ratings for each age group
#         formatted_data = []
#         for age_group, phases in age_ratings.items():
#             pre_avg = sum(phases["pre"]) / len(phases["pre"]) if phases["pre"] else 0
#             post_avg = sum(phases["post"]) / len(phases["post"]) if phases["post"] else 0
#             print(f"Age Group: {age_group}, Pre Avg: {pre_avg}, Post Avg: {post_avg}")
            
#             formatted_data.append({
#                 "age_group": age_group,
#                 "pre": pre_avg,
#                 "post": post_avg
#             })

#         print("Final computed data:", formatted_data)
#         return Response({"data": formatted_data}, status=200)

#     except Company.DoesNotExist:
#         print(f"Error: Company with ID {company_id} not found.")
#         return Response({"error": "Company not found"}, status=404)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_demographic_vs_survey_improvement(request, company_id, demographic_type):
    """Fetches average survey ratings split by demographic type (age, salary, education, etc.), comparing pre vs post responses."""

    try:
        print(f"Fetching {demographic_type} vs survey improvement data for company ID: {company_id}")

        # Get the corresponding Korean question text
        korean_question_text = get_korean_question(demographic_type)
        if not korean_question_text:
            return Response({"error": "Invalid demographic category"}, status=400)

        # Fetch company and users
        company = Company.objects.get(id=company_id)
        users = User.objects.filter(company=company)
        print(f"Company found: {company.name}, Total users: {users.count()}")

        # Get the question object of the demographic type
        question = Question.objects.filter(text__icontains=korean_question_text).first()
        if not question:
            return Response({"error": f"Question not found for {demographic_type}"}, status=404)

        print(f"Demographic question ID: {question.id}, Text: {question.text}")

        # Get user answers for the category questions
        answers = Answer.objects.filter(question=question, response__user__in=users)
        print(f"Total {demographic_type} responses found: {answers.count()} answers: {answers}")

        # Map user IDs to their category value (age, salary, etc.) each user is assigned to a category
        user_categories = {ans.response.user.id: ans.answer_text for ans in answers}

        # Process all answers (no filtering)
        survey_answers = Answer.objects.filter(response__user__in=users) # get answers of the users
        print(f"Processing {survey_answers.count()} total answers.")

        category_ratings = defaultdict(lambda: {"pre": [], "post": []})

        for ans in survey_answers:
            user_id = ans.response.user.id # get user id for each answer
            category = user_categories.get(user_id, "Unknown") # get category group of the user
            phase = ans.response.phase  # 'pre' or 'post'

            if ans.answer_value is not None:
                category_ratings[category][phase].append(ans.answer_value) # add the value to the phase of the category

        # Compute average ratings
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

        return Response({"data": formatted_data}, status=200)

    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=404)

    """
    API view to return survey improvement data for different demographic types.
    Example: /api/companies/{company_id}/demographic-improvement/age/
    """

    data = get_demographic_vs_survey_improvement(company_id, demographic_type)
    print("Data:", data)
    if "error" in data:
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    return Response(data, status=status.HTTP_200_OK)
CATEGORIES = ["entrepreneur", "org", "selflead", "ppc", "lifestyle"]

@api_view(["GET"])
@permission_classes([AllowAny])
def get_company_vs_industry_growth(request, company_id):
    """
    Computes the average percentage increase in survey scores for different categories:
    - One line represents percentage growth for the company.
    - Another line represents percentage growth for all users.
    """

    try:
        print(f"\n🔹 Fetching growth data for Company ID: {company_id}")

        # Get company and users
        company = Company.objects.get(id=company_id)
        company_users = User.objects.filter(company=company)
        all_users = User.objects.all()

        print(f"✅ Company Found: {company.name}")
        print(f"👥 Total Company Users: {company_users.count()}, Total All Users: {all_users.count()}")

        def calculate_growth(users, user_type="Company"):
            """
            Given a queryset of users, compute the average percentage increase
            for each category by comparing pre-survey and post-survey values.
            """
            responses = UserSurveyResponse.objects.filter(user__in=users)
            answers = Answer.objects.filter(response__in=responses)

            print(f"\n📊 Calculating {user_type} Growth | Total Responses: {responses.count()}, Total Answers: {answers.count()}")

            growth_data = defaultdict(float)  # Default to 0 if category has no data

            for category in CATEGORIES:
                questions = Question.objects.filter(category__icontains=category)
                category_answers = answers.filter(question__in=questions)

                print(f"🔎 Category: {category} | Questions Found: {questions.count()} | Answers Found: {category_answers.count()}")

                # Compute pre-survey and post-survey averages
                pre_avg = category_answers.filter(response__phase="pre").aggregate(Avg("answer_value"))["answer_value__avg"]
                post_avg = category_answers.filter(response__phase="post").aggregate(Avg("answer_value"))["answer_value__avg"]

                if pre_avg is None or post_avg is None:
                    print(f"⚠️ No valid data for {category}. Defaulting growth to 0%.")
                    growth_data[category] = 0
                    continue

                # Calculate percentage growth
                if pre_avg > 0:
                    growth = ((post_avg - pre_avg) / pre_avg) * 100
                else:
                    growth = 0

                growth_data[category] = growth
                print(f"📈 {user_type} Growth for {category}: {growth:.2f}% (Pre: {pre_avg:.2f}, Post: {post_avg:.2f})")

            return dict(growth_data)

        # Calculate growth for company users and all users
        company_growth = calculate_growth(company_users, "Company")
        industry_growth = calculate_growth(all_users, "Industry")

        # Prepare response data
        response_data = {
            "categories": CATEGORIES,
            "company_scores": [company_growth.get(cat, 0) for cat in CATEGORIES],
            "industry_scores": [industry_growth.get(cat, 0) for cat in CATEGORIES]
        }

        print("\n✅ Final Computed Growth Data:", response_data)

        return Response(response_data, status=200)

    except Company.DoesNotExist:
        print("❌ Error: Company not found.")
        return Response({"error": "Company not found"}, status=404)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_lifestyle_vs_performance_growth(request, company_id):
    """
    Computes overall performance growth based on lifestyle question ratings.

    This function creates data for a heatmap where:
    - **X-axis**: Lifestyle-related questions.
    - **Y-axis**: Ratings (1-5).
    - **Cell values**: Percentage increase in overall performance for users who picked that rating.

    Steps:
    1. Identify users who selected each rating (1-5) for each lifestyle question.
    2. Fetch **all** their survey responses (not just lifestyle).
    3. Calculate their overall pre-survey & post-survey average across all answers.
    4. Compute percentage growth and return structured data.

    ---
    **Output Format:**
    ```json
    {
        "data": [
            {
                "question": "나는 건강을 위해 운동한다.",
                "rating": 5,
                "growth": 18.75
            },
            {
                "question": "나는 새로운 도전을 즐긴다.",
                "rating": 3,
                "growth": -6.45
            },
            ...
        ]
    }
    ```
    - `question`: The lifestyle-related question.
    - `rating`: The specific rating (1-5) chosen by users.
    - `growth`: Percentage increase in overall performance for users who picked this rating.
    """
    try:
        print(f"Fetching lifestyle vs performance growth data for company ID: {company_id}")

        # Step 1: Get company and users
        company = Company.objects.get(id=company_id)
        users = User.objects.filter(company=company)
        print(f"Company found: {company.name}, Total users: {users.count()}")

        # Step 2: Fetch all lifestyle-related questions
        lifestyle_questions = Question.objects.filter(category="lifestyle")
        if not lifestyle_questions.exists():
            return Response({"error": "No lifestyle questions found"}, status=404)

        print(f"Total lifestyle questions found: {lifestyle_questions.count()}")

        # Step 3: Fetch all answers related to lifestyle questions for users in this company
        responses = UserSurveyResponse.objects.filter(user__in=users)
        lifestyle_answers = Answer.objects.filter(response__in=responses, question__in=lifestyle_questions)

        print(f"Total lifestyle responses found: {lifestyle_answers.count()}")

        # Step 4: Store rating-based user groups
        rating_users_map = defaultdict(lambda: defaultdict(set))

        for ans in lifestyle_answers:
            user_id = ans.response.user.id
            question_text = ans.question.text
            rating = int(ans.answer_value) if ans.answer_value else None

            if rating and 1 <= rating <= 5:
                rating_users_map[question_text][rating].add(user_id)

                # Debugging: Track which users picked which rating for which question
                print(f"User {ans.response.user.name} (ID={user_id}) chose rating {rating} for '{question_text}'")

        # Step 5: Compute growth for each (question, rating) pair
        formatted_data = []

        for question, rating_map in rating_users_map.items():
            for rating, user_ids in rating_map.items():
                if not user_ids:
                    continue

                # Step 6: Fetch all responses (not just lifestyle) for these users
                user_responses = UserSurveyResponse.objects.filter(user_id__in=user_ids)
                all_answers = Answer.objects.filter(response__in=user_responses)

                # Calculate pre & post survey averages
                pre_avg = all_answers.filter(response__phase="pre").aggregate(Avg("answer_value"))["answer_value__avg"] or 0
                post_avg = all_answers.filter(response__phase="post").aggregate(Avg("answer_value"))["answer_value__avg"] or 0

                percentage_growth = ((post_avg - pre_avg) / pre_avg) * 100 if pre_avg else 0

                # Debugging: Show calculated values for each (question, rating) pair
                print(f"Question: '{question}', Rating: {rating}, Users: {len(user_ids)}, Pre Avg: {pre_avg}, Post Avg: {post_avg}, Growth: {percentage_growth:.2f}%")

                formatted_data.append({
                    "question": question,
                    "rating": rating,
                    "growth": percentage_growth
                })

        return Response({"data": formatted_data}, status=200)

    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=404)