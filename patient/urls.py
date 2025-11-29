from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.profile_view, name='patient_profile'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
