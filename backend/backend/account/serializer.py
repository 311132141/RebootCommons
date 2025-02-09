from rest_framework import serializers
from .models import User, Company  # Import your models

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer()  # Nested serializer

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'company']
