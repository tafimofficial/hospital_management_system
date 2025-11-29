from django.urls import path
from . import views

urlpatterns = [
    path('', views.blood_bank_home, name='blood_bank_home'),
    path('donate/', views.register_donor, name='register_donor'),
    path('request/', views.request_blood, name='request_blood'),
    path('donors/', views.find_donors, name='find_donors'),
]
