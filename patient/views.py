from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import PatientProfile
from doctor.models import DoctorProfile, Appointment
from .forms import PatientProfileForm, AppointmentForm
from blood_bank.models import BloodRequest
from core.notifications import notify_user

@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('home')
    
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
    blood_requests = BloodRequest.objects.filter(user=request.user).order_by('-request_date')
    return render(request, 'patient/dashboard.html', {
        'appointments': appointments,
        'blood_requests': blood_requests
    })

@login_required
@never_cache
def profile_view(request):
    if not request.user.is_patient:
        return redirect('home')
    return render(request, 'patient/profile.html')

@login_required
def book_appointment(request):
    if not request.user.is_patient:
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            
            # Notify doctor
            notify_user(
                user=appointment.doctor.user,
                title='New Appointment Request',
                message=f'{request.user.get_full_name()} has requested an appointment on {appointment.date} at {appointment.time}.',
                notification_type='appointment',
                related_object_id=appointment.id,
                link='/doctor/dashboard/'
            )
            
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    
    return render(request, 'patient/book_appointment.html', {'form': form})

@login_required
def edit_profile(request):
    if not request.user.is_patient:
        return redirect('home')
    
    profile = request.user.patient_profile
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('patient_dashboard')
    else:
        form = PatientProfileForm(instance=profile)
    
    return render(request, 'patient/edit_profile.html', {'form': form})
