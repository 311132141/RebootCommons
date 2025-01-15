from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })
    
    if form.is_valid():
        form.save()
        print({'message': 'success'})  # Example of success response

        return JsonResponse({'message': 'success'}, status=201)
    else:
        return JsonResponse({'message': 'error', 'errors': form.errors}, status=400)