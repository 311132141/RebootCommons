from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import UserSurvey

User = get_user_model()

class SurveyAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Test User",  # Provide the name
            email="testuser@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_survey(self):
        data = {
            "gender": "male",
            "age": 30,
            "marital_status": "single",
            "education": "bachelor"
        }
        response = self.client.post("/api/survey/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_survey(self):
        UserSurvey.objects.create(user=self.user, gender="male", age=30, marital_status="single", education="bachelor")
        response = self.client.get("/api/survey/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['age'], 30)
