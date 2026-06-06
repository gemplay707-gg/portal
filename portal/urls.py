from django.urls import path
from .views import HomePageView, SignUpView, ProfileView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
]