from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm
from .models import Company, User
from collections import Counter
from .serializer import UserSerializer, CompanySerializer, CompanyExplanationSerializer, UserExplanationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import CompanyExplanation, UserExplanation
from rest_framework.views import APIView
from rest_framework import status
from survey.models import CourseType

@api_view(['GET'])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)  # ✅ DRF handles JSON conversion


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    company_name = data.get('company')
    company = None

    # Check if a company name is provided
    if company_name:
        company, created = Company.objects.get_or_create(name=company_name)

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
        'company': company if company else None
    })

    if form.is_valid():
        user = form.save(commit=False)
        user.company = company
        user.save()
        return JsonResponse({'message': 'success'}, status=201)
    else:
        return JsonResponse({'message': 'error', 'errors': form.errors}, status=400)
    
@api_view(['GET'])
def get_companies(request):
    companies = Company.objects.all()
    data = [
        {
            "id": company.id,
            "name": company.name,
            "email": company.email,
            "phone": company.phone_number,
            "course_type": company.course_type.name if company.course_type else "No Course Type Assigned",
            "growth": "20%"  # Placeholder, replace with actual logic
        }
        for company in companies
    ]
    return JsonResponse({"companies": data}, safe=False)

@api_view(['GET'])
def get_company_users(request, company_id):
    """Fetch all users for a given company."""
    try:
        company_instance = Company.objects.get(id=company_id)
        users = User.objects.filter(company=company_instance)  # Assuming users store company name as a string
        
        data = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "avatar": user.avatar.url if user.avatar else None,
            }
            for user in users
        ]
        return JsonResponse({"company": company_instance.name, "users": data}, safe=False)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)

@api_view(['GET'])
def get_company_dashboard(request, company_id):
    """
    Fetch aggregated data (e.g., gender distribution, leadership roles)
    for a company's dashboard.
    """

    try:
        # Retrieve the company
        company = Company.objects.get(id=company_id)

        # Get users in this company
        users = User.objects.filter(company=company)

        # Count gender distribution
        gender_counts = Counter(user.gender for user in users if user.gender)

        # Count leadership roles
        leadership_roles = Counter(user.role for user in users if user.role)

        # Format the data for Vue
        data = {
            "company": company.name,
            "total_users": users.count(),
            "gender_distribution": gender_counts,
            "leadership_roles": leadership_roles,
        }

        return JsonResponse(data, safe=False)

    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)
    
class CompanyExplanationView(generics.RetrieveUpdateAPIView):
    """
    GET: Retrieve the explanation for a company
    PUT/PATCH: Update the explanation for a company
    """
    serializer_class = CompanyExplanationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # 1) Fetch the company (or 404)
        company_id = self.kwargs.get('company_id')
        company = get_object_or_404(Company, id=company_id)
        
        # 2) Get or create the explanation row
        obj, created = CompanyExplanation.objects.get_or_create(company=company)
        return obj
    
class UserExplanationView(generics.RetrieveUpdateAPIView):
    """
    GET: Retrieve the explanation for a user
    PUT/PATCH: Update the explanation for a user
    """
    serializer_class = UserExplanationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 1) Fetch the user (or 404)
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        # 2) Get or create the explanation row
        obj, created = UserExplanation.objects.get_or_create(user=user)
        return obj
    
class CompanyRegisterView(APIView):
    permission_classes = []  # Allow any (adjust permissions as needed)

    def post(self, request, *args, **kwargs):
        company_name = request.data.get('name')
        course_name = request.data.get('course')
        if not company_name or not course_name:
            return Response(
                {"error": "회사 이름과 코스 선택은 필수입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Look up the CourseType
        try:
            course_type = CourseType.objects.get(name=course_name, survey_type__name="기업용")
        except CourseType.DoesNotExist:
            return Response(
                {"error": f"코스 '{course_name}'가 존재하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create or update the company
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={'course_type': course_type}
        )
        if not created and company.course_type != course_type:
            company.course_type = course_type
            company.save()
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)