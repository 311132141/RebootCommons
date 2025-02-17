# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from account.models import Company
from .models import SurveyType, CourseType, SurveyTypeQuestion, CourseTypeQuestion, Question, Answer, UserSurveyResponse

User = get_user_model()

class SurveyAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test company
        cls.company = Company.objects.create(
            name="Test Company",
            email="testcompany@example.com",
            phone_number="010-1234-5678"
        )

        # Create SurveyType and CourseType objects
        cls.survey_type = SurveyType.objects.create(
            name="개인용",
            description="Personal usage"
        )
        cls.course_type = CourseType.objects.create(
            name="비전하우스",
            description="Test course",
            survey_type=cls.survey_type
        )

        # Create test questions
        cls.question1 = Question.objects.create(
            text="Test Question 1",
            category="selflead"
        )
        cls.question2 = Question.objects.create(
            text="라이프스타일: 1. 내가 희망하더라도 지금 당장 회사를 그만두기는 어렵다.",
            category="lifestyle"
        )

        # Create bridging objects
        cls.st_question = SurveyTypeQuestion.objects.create(
            survey_type=cls.survey_type,
            question=cls.question1,
            order=1
        )
        cls.ct_question = CourseTypeQuestion.objects.create(
            course_type=cls.course_type,
            question=cls.question2,
            order=1
        )

        # Create a test user assigned to the company
        cls.user = User.objects.create_user(
            name="Test User",
            email="testuser@example.com",
            password="testpassword",
            company=cls.company
        )

        # Create a pre-phase response for the test user
        cls.pre_response = UserSurveyResponse.objects.create(
            user=cls.user,
            survey_type=cls.survey_type,
            course_type=cls.course_type,
            phase="pre"
        )
        cls.answer1 = Answer.objects.create(
            response=cls.pre_response,
            question=cls.question1,
            answer_text="Pre Answer",
            answer_value=3
        )

        # Create a post-phase response for the test user
        cls.post_response = UserSurveyResponse.objects.create(
            user=cls.user,
            survey_type=cls.survey_type,
            course_type=cls.course_type,
            phase="post"
        )
        cls.answer2 = Answer.objects.create(
            response=cls.post_response,
            question=cls.question1,
            answer_text="Post Answer",
            answer_value=4
        )

        # Setup API client and force authentication
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)

    def test_survey_type_list(self):
        url = reverse('survey_type_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_course_type_list(self):
        url = reverse('course_type_courses', args=[self.survey_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_survey_view_get(self):
        url = reverse('survey_view', args=[self.survey_type.id, self.course_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_survey_view_post_pre(self):
        # Create a new user with no pre-phase response
        new_user = User.objects.create_user(
            name="New User",
            email="newuser@example.com",
            password="newpassword",
            company=self.company
        )
        client = APIClient()
        client.force_authenticate(user=new_user)
        url = reverse('survey_view', args=[self.survey_type.id, self.course_type.id])
        data = {
            "answers": [
                {"question_id": self.question1.id, "answer_text": "New Pre Answer", "answer_value": 4}
            ]
        }
        response = client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("phase"), "pre")

    def test_survey_view_post_post(self):
        # The test user already has a pre response, so new submission should be post-phase.
        url = reverse('survey_view', args=[self.survey_type.id, self.course_type.id])
        data = {
            "answers": [
                {"question_id": self.question1.id, "answer_text": "New Post Answer", "answer_value": 5},
                {"question_id": self.question2.id, "answer_text": "Skipped Answer", "answer_value": 3}
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("phase"), "post")

    def test_gender_distribution(self):
        url = reverse('gender-distribution')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("labels", response.data)
        self.assertIn("datasets", response.data)

    def test_age_distribution(self):
        url = reverse('age-distribution')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("labels", response.data)
        self.assertIn("datasets", response.data)

    def test_get_gender_vs_leadership(self):
        url = reverse('gender-leadership', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_get_demographic_vs_survey_improvement(self):
        # Assume the endpoint name is 'demographic-improvement'
        url = reverse('demographic-improvement', args=[self.company.id, "age"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_get_company_vs_industry_growth(self):
        url = reverse('growth-comparison', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categories", response.data)

    def test_get_lifestyle_vs_performance_growth(self):
        url = reverse('lifestyle-performance-growth', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
