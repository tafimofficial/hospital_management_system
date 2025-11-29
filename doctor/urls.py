from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.profile_view, name='doctor_profile'),
    path('appointment/approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('appointment/decline/<int:appointment_id>/', views.decline_appointment, name='decline_appointment'),
    path('edit-profile/', views.edit_profile, name='edit_doctor_profile'),
]
