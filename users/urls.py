from django.urls import path
from .views import LoginView, RegisterView, ProfileView, LogoutView, UserUpdateView

app_name='users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='profile_edit'),


]