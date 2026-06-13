from django.urls import path
from .views import (
    home_page, SignUpView, ProfileView, edit_profile,
    classes_dashboard, create_class, join_class, class_room
)

urlpatterns = [
    path('', home_page, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    path('classes/', classes_dashboard, name='classes_dashboard'),
    path('classes/create/', create_class, name='create_class'),
    path('classes/join/', join_class, name='join_code_class'),
    path('classes/join/<int:class_id>/', join_class, name='join_public_class'),
    path('classes/<int:class_id>/', class_room, name='class_room'),
]