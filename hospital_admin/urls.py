from django.urls import path
from . import views, blood_views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-doctors/', views.manage_doctors, name='manage_doctors'),
    path('manage-patients/', views.manage_patients, name='manage_patients'),
    
    # Doctor approval
    path('doctor/approve/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('doctor/reject/<int:doctor_id>/', views.reject_doctor, name='reject_doctor'),
    
    # User management
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Services
    path('services/', views.manage_services, name='manage_services'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),

    # Blood Bank Admin
    path('blood-bank/', blood_views.manage_blood_bank, name='manage_blood_bank'),
    path('blood-bank/update/<int:pk>/', blood_views.update_blood_inventory, name='update_blood_inventory'),
    path('blood-bank/request/<int:pk>/', blood_views.manage_blood_request, name='manage_blood_request'),
    path('blood-bank/donor/<int:pk>/', blood_views.manage_blood_donor, name='manage_blood_donor'),
]
