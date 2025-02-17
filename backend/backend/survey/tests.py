# tests.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from account.models import Company
from survey.models import (
    SurveyType, CourseType, SurveyTypeQuestion, CourseTypeQuestion,
    Question, Answer, UserSurveyResponse
)

User = get_user_model()

class SurveyAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test company with a valid course type.
        cls.company = Company.objects.create(
            name="Test Company",
            email="company@test.com",
            phone_number="1234567890"
        )
        # For testing get_company_vs_industry_growth, we need the company to have a course_type
        # that is recognized by get_company_categories. Let's assume "비전하우스" is valid.
        cls.course_type = CourseType.objects.create(
            name="비전하우스",
            description="Test course",
            survey_type=SurveyType.objects.create(
                name="기업용",  # Set survey type to "기업용" so that our mapping in get_categories_by_course_type works.
                description="Corporate usage"
            )
        )
        cls.company.course_type = cls.course_type
        cls.company.save()

        # Create test questions.
        # Question for general survey:
        cls.question1 = Question.objects.create(
            text="Test Question 1",
            category="selflead"
        )
        # Lifestyle question:
        cls.question2 = Question.objects.create(
            text="라이프스타일: 1. 내가 희망하더라도 지금 당장 회사를 그만두기는 어렵다.",
            category="lifestyle"
        )
        # Gender question (for get_gender_vs_leadership)
        cls.gender_question = Question.objects.create(
            text="귀하의 성별은?",
            category="demographic"
        )

        # Create bridging objects.
        cls.st_question = SurveyTypeQuestion.objects.create(
            survey_type=cls.course_type.survey_type,
            question=cls.question1,
            order=1
        )
        cls.ct_question = CourseTypeQuestion.objects.create(
            course_type=cls.course_type,
            question=cls.question2,
            order=1
        )

        # Create a bridging object for gender question so that it is linked to the survey.
        cls.gender_st_question = SurveyTypeQuestion.objects.create(
            survey_type=cls.course_type.survey_type,
            question=cls.gender_question,
            order=2
        )

        # Create a test user assigned to the company.
        cls.user = User.objects.create_user(
            name="Test User",
            email="testuser@test.com",
            password="testpass123",
            company=cls.company
        )

        # Create a pre-phase response for the test user.
        cls.pre_response = UserSurveyResponse.objects.create(
            user=cls.user,
            survey_type=cls.course_type.survey_type,
            course_type=cls.course_type,
            phase="pre"
        )
        cls.answer1 = Answer.objects.create(
            response=cls.pre_response,
            question=cls.question1,
            answer_text="Pre Answer",
            answer_value=3
        )
        cls.gender_answer = Answer.objects.create(
            response=cls.pre_response,
            question=cls.gender_question,
            answer_text="남성",
            answer_value=None
        )

        # Create a post-phase response for the test user.
        cls.post_response = UserSurveyResponse.objects.create(
            user=cls.user,
            survey_type=cls.course_type.survey_type,
            course_type=cls.course_type,
            phase="post"
        )
        cls.answer2 = Answer.objects.create(
            response=cls.post_response,
            question=cls.question1,
            answer_text="Post Answer",
            answer_value=4
        )

        # Setup APIClient and force authentication for the tests.
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)

    def test_survey_type_list(self):
        url = reverse('survey_type_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_course_type_list(self):
        url = reverse('course_type_courses', args=[self.course_type.survey_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_survey_view_get(self):
        url = reverse('survey_view', args=[self.course_type.survey_type.id, self.course_type.id])
        response = self.client.get(url)
        # Expect lifestyle questions to be filtered out for authenticated users
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=f"Response data: {response.data}")

        # Ensure no question with category "lifestyle" is returned.
        for q in response.data:
            self.assertNotEqual(q.get("category"), "lifestyle")
            self.assertNotEqual(q.get("category"), "demographic")

    def test_survey_view_post_pre(self):
        # Create a new user with no pre-phase response.
        new_user = User.objects.create_user(
            name="New User",
            email="newuser@test.com",
            password="newpass123",
            company=self.company
        )
        client = APIClient()
        client.force_authenticate(user=new_user)
        url = reverse('survey_view', args=[self.course_type.survey_type.id, self.course_type.id])
        data = {
            "answers": [
                {"question_id": self.question1.id, "answer_text": "New Pre Answer", "answer_value": 4}
            ]
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=f"Response data: {response.data}")
        self.assertEqual(response.data.get("phase"), "pre")

    def test_survey_view_post_post(self):
        # Test user already has a pre response so new submission should be post-phase.
        url = reverse('survey_view', args=[self.course_type.survey_type.id, self.course_type.id])
        data = {
            "answers": [
                {"question_id": self.question1.id, "answer_text": "New Post Answer", "answer_value": 5},
                # Lifestyle answer should be skipped on post-phase.
                {"question_id": self.question2.id, "answer_text": "Should be skipped", "answer_value": 3}
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=f"Response data: {response.data}")
        self.assertEqual(response.data.get("phase"), "post", msg=f"Response data: {response.data}")



    def test_get_gender_vs_leadership(self):
        url = reverse('gender-leadership', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_get_demographic_vs_survey_improvement(self):
        # Ensure URL name is correct (added name="demographic-improvement" in urls.py)
        url = reverse('demographic-improvement', args=[self.company.id, "age"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=f"Response data: {response.data}")
        self.assertIn("data", response.data)

    def test_get_company_vs_industry_growth(self):
        url = reverse('growth-comparison', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categories", response.data)

    def test_get_lifestyle_vs_performance_growth(self):
        url = reverse('lifestyle-performance-growth', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=f"Response data: {response.data}")

        self.assertIn("data", response.data)

    def test_get_user_profile(self):
        url = reverse('user-profile', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertIn("demographics", response.data)

    def test_get_user_pre_post_comparison(self):
        url = reverse('user-pre-post-comparison', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categories", response.data)

    def test_get_user_vs_all_growth(self):
        url = reverse('user-growth-comparison', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categories", response.data)

    def test_get_all_users_lifestyle_performance_growth(self):
        url = reverse('all-users-lifestyle-performance-growth')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=f"Response data: {response.data}")

        self.assertIn("data", response.data)

    def test_get_user_question_pre_post_comparison(self):
        url = reverse('user-question-pre-post-comparison', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categories", response.data)

    def test_get_company_statistics(self):
        url = reverse('company-statistics', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_count", response.data)
        self.assertIn("average_growth", response.data)
        self.assertIn("course_type", response.data)

    def test_get_users_without_company(self):
        url = reverse('users_without_company')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for user_data in response.data:
            self.assertIsNone(user_data.get("company"))

