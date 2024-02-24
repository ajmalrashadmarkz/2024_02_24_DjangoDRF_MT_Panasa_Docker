from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from .views import UserCreateView, UserLoginView,UserLogoutView
urlpatterns = [
    
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
    path('users/logout/', csrf_exempt(UserLogoutView.as_view()), name='user-logout'),
]