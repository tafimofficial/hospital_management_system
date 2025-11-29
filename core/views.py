from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db.models import Q
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from doctor.models import DoctorProfile
from hospital_admin.models import Service

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.is_patient:
            return redirect('patient_dashboard')
        elif request.user.is_doctor:
            return redirect('doctor_dashboard')
    return render(request, 'home.html')

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'core/register_patient.html', {'form': form, 'title': 'Patient Registration'})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Doctor is not logged in immediately because status is pending
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'core/register_doctor.html', {'form': form, 'title': 'Doctor Registration'})

def find_doctors(request):
    doctors = DoctorProfile.objects.filter(status='active')
    
    # Get all unique specializations for filter dropdown
    specializations = DoctorProfile.objects.filter(status='active').values_list('specialization', flat=True).distinct()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )
    
    # Filter by specialization
    specialization_filter = request.GET.get('specialization', '')
    if specialization_filter:
        doctors = doctors.filter(specialization=specialization_filter)
    
    context = {
        'doctors': doctors,
        'specializations': specializations,
        'search_query': search_query,
        'specialization_filter': specialization_filter,
    }
    return render(request, 'core/find_doctors.html', context)

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id, status='active')
    return render(request, 'core/doctor_detail.html', {'doctor': doctor})

def services_page(request):
    services = Service.objects.filter(is_active=True)
    
    # Get all categories
    categories = Service.CATEGORY_CHOICES
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        services = services.filter(category=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'services': services,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    return render(request, 'core/services.html', context)
