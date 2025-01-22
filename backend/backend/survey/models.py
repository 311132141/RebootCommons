from django.db import models
from account.models import User
import uuid


class UserSurvey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to the user
    survey_type = models.CharField(
        max_length=20,
        choices=[('기업용', '기업용'), ('개인용', '개인용')],
        default='개인용'
    )
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    age = models.IntegerField(choices=[(20, '20s'), (30, '30s'), (40, '40s'), (50, '50s'), (60, '60s')])
    marital_status = models.CharField(max_length=10, choices=[('single', 'Single'), ('married', 'Married')])
    education = models.CharField(
        max_length=20,
        choices=[
            ('highschool', 'High School'),
            ('diploma', 'Diploma'),
            ('bachelor', 'Bachelor'),
            ('master', 'Master'),
            ('phd', 'PhD'),
        ],
    )
    # Properly defined `course_type` field
    course_type = models.CharField(
        max_length=20,
        choices=[
            ('비전하우스', '비전하우스'),
            ('리더십', '리더십'),
            ('기업가정신', '기업가정신'),
        ],
        default='비전하우스'
    )
    is_pre_lecture = models.BooleanField(default=True)  # True for pre-lecture, False for post-lecture
    answers = models.JSONField(default=dict)  # Store dynamic answers as a JSON object

    def __str__(self):
        return f"{self.user.name if self.user else 'Anonymous User'} - {self.survey_type}"
