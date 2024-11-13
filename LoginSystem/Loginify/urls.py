from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),

    # CRUD API URL patterns
    path('api/users/', views.get_all_users, name='get_all_users'),
    path('api/users/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
    path('api/users/update/<str:email>/', views.update_user, name='update_user'),
    path('api/users/delete/<str:email>/', views.delete_user, name='delete_user'),
]