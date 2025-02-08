
from django.db import models
from account.models import User  
import uuid


# SurveyType: Personal or Corporate
class SurveyType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# CourseType: Tied to SurveyType (e.g., 비전하우스)
class CourseType(models.Model):
    survey_type = models.ForeignKey(SurveyType, on_delete=models.CASCADE, related_name='course_types')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.survey_type.name})"


# Question: Stores question details
class Question(models.Model):
    QUESTION_TYPES = [
        ('rating', 'Rating'),
        ('text', 'Text'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
    ]

    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='rating')
    options = models.JSONField(blank=True, null=True)  # Store options as JSON (if applicable)
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.text


# Bridging table: Questions tied to SurveyType
class SurveyTypeQuestion(models.Model):
    survey_type = models.ForeignKey(SurveyType, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(default=True)

    class Meta:
        unique_together = ('survey_type', 'question', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.survey_type.name}: {self.question.text}"


# Bridging table: Questions tied to CourseType
class CourseTypeQuestion(models.Model):
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(default=True)

    class Meta:
        unique_together = ('course_type', 'question', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.course_type.name}: {self.question.text}"


# Survey Response (User's answers for a given survey)
class UserSurveyResponse(models.Model):
    PHASE_CHOICES = [
        ('pre', 'Pre-Lecture'),
        ('post', 'Post-Lecture'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    survey_type = models.ForeignKey(SurveyType, on_delete=models.CASCADE)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    phase = models.CharField(max_length=10, choices=PHASE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}: {self.survey_type.name} - {self.course_type.name} ({self.phase})"


# Answer: Records individual question responses
class Answer(models.Model):
    response = models.ForeignKey(UserSurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)
    answer_value = models.IntegerField(blank=True, null=True)  # For rating questions

    def __str__(self):
        return f"Answer to {self.question.text} by {self.response.user.name}"
