from django.db import models
from account.models import User
import uuid


# Create your models here.
class UserSurvey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to the user
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
    # Add other fields for questions here...

    def __str__(self):
        return self.user.name if self.user else "Anonymous Survey"
