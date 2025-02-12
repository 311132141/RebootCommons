from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm
from .models import Company, User
from collections import Counter
from .serializer import UserSerializer
from rest_framework.response import Response

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

    company_name = data.get('company_name')
    company = None

    # Check if a company name is provided
    if company_name:
        company, created = Company.objects.get_or_create(name=company_name)

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
        'company': company.id if company else None
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