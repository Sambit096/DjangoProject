from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from .models import UserDetails
import json
# Create your views here.
def home(request):
    return redirect('login')  # Redirect to login page or render a home template

#Implementing Signup view
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        else:
            hashed_password = make_password(password)
            user = UserDetails(username=username, email=email, password=hashed_password)
            user.save()
            messages.success(request, 'Signup successful. Please login.')
            return redirect('login')  # Redirect to login page upon successful signup
    else:
        return render(request, 'Loginify/signup.html')
    
#Implementing Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserDetails.objects.get(email=email)
            if check_password(password, user.password):
                messages.success(request, f'Welcome, {user.username}!')
                return render(request, 'Loginify/success.html', {'user': user})  # Display success message
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
        except UserDetails.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    else:
        return render(request, 'Loginify/login.html')
    
def success_view(request):
    # This view can be used to render the success page directly if needed
    return render(request, 'Loginify/success.html')

#Implementing GetAllUsers View
@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = UserDetails.objects.all()
        users_list = []
        for user in users:
            users_list.append({
                'username': user.username,
                'email': user.email,
                # Password is intentionally excluded
            })
        return JsonResponse({'users': users_list})
    else:
        return HttpResponseNotAllowed(['GET'])

#Implementing GetUserByEmail View
@csrf_exempt
def get_user_by_email(request, email):
    if request.method == 'GET':
        try:
            user = UserDetails.objects.get(email=email)
            user_data = {
                'username': user.username,
                'email': user.email,
                # Do not include the password
            }
            return JsonResponse({'user': user_data})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['GET'])

#Update User Details View 
@csrf_exempt
def update_user(request, email):
    if request.method == 'PUT':
        try:
            user = UserDetails.objects.get(email=email)
            data = json.loads(request.body)

            # Do not change the primary key (username)
            password = data.get('password', None)

            if password:
                from django.contrib.auth.hashers import make_password
                user.password = make_password(password)
                user.save()
                return JsonResponse({'message': 'Password updated successfully'})
            else:
                return JsonResponse({'message': 'No changes made'})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])
    
#Delete a User Using Its Email View
@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])