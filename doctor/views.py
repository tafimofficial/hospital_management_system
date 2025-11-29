from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import DoctorProfile, Appointment
from .forms import DoctorProfileForm

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        return redirect('home')
    
    doctor_profile = request.user.doctor_profile
    if doctor_profile.status != 'active':
        return render(request, 'doctor/pending_approval.html')

    appointments = Appointment.objects.filter(doctor=doctor_profile).order_by('-date', '-time')
    return render(request, 'doctor/dashboard.html', {'appointments': appointments})

@login_required
@never_cache
def profile_view(request):
    if not request.user.is_doctor:
        return redirect('home')
    return render(request, 'doctor/profile.html')

@login_required
def approve_appointment(request, appointment_id):
    if not request.user.is_doctor:
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)
    appointment.status = 'approved'
    appointment.save()
    messages.success(request, 'Appointment approved successfully!')
    return redirect('doctor_dashboard')

@login_required
def decline_appointment(request, appointment_id):
    if not request.user.is_doctor:
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)
    appointment.status = 'declined'
    appointment.save()
    messages.success(request, 'Appointment declined successfully!')
    return redirect('doctor_dashboard')

@login_required
def edit_profile(request):
    if not request.user.is_doctor:
        return redirect('home')
    
    profile = request.user.doctor_profile
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctor_dashboard')
    else:
        form = DoctorProfileForm(instance=profile)
    
    return render(request, 'doctor/edit_profile.html', {'form': form})
