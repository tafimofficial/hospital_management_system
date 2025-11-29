from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .password_views import change_password
from .notification_views import get_notifications, mark_notification_read, mark_all_read, all_notifications

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_page, name='services'),
    path('doctors/', views.find_doctors, name='find_doctors'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('change-password/', change_password, name='change_password'),
    
    # Notification URLs
    path('notifications/', all_notifications, name='all_notifications'),
    path('api/notifications/', get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', mark_all_read, name='mark_all_read'),
]
