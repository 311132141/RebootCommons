from rest_framework import serializers
from .models import *
from survey.models import CourseType  # Import CourseType

class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = ['id', 'name']  # Only return necessary fields

class CompanySerializer(serializers.ModelSerializer):
    course_type = CourseTypeSerializer()  # Nest CourseType details

    class Meta:
        model = Company
        fields = ['id', 'name', 'course_type']

class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer()  # Nest Company details

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'company', 'is_superuser']

class CompanyExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyExplanation
        fields = ['company', 'explanation_text', 'updated_at']
        read_only_fields = ['company', 'updated_at']

class UserExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExplanation
        fields = ['user', 'explanation_text', 'updated_at']
        read_only_fields = ['user', 'updated_at']
