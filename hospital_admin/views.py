from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from core.models import User
from doctor.models import DoctorProfile, Appointment
from patient.models import PatientProfile
from .models import Service
from .forms import ServiceForm
from core.notifications import notify_user

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    pending_doctors = DoctorProfile.objects.filter(status='pending')
    total_doctors = DoctorProfile.objects.count()
    total_patients = PatientProfile.objects.count()
    total_appointments = Appointment.objects.count()
    
    context = {
        'pending_doctors': pending_doctors,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
    }
    return render(request, 'hospital_admin/dashboard.html', context)

@user_passes_test(is_admin)
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor.status = 'active'
    doctor.save()
    
    # Notify doctor
    notify_user(
        user=doctor.user,
        title='Doctor Profile Approved',
        message='Congratulations! Your doctor profile has been approved. You can now start managing appointments.',
        notification_type='doctor_approval',
        link='/doctor/dashboard/'
    )
    
    messages.success(request, f'Dr. {doctor.user.get_full_name()} approved successfully!')
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def reject_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor.status = 'rejected'
    doctor.save()
    
    # Notify doctor
    notify_user(
        user=doctor.user,
        title='Doctor Profile Rejected',
        message='Unfortunately, your doctor profile application has been rejected. Please contact admin for more information.',
        notification_type='doctor_approval'
    )
    
    messages.success(request, f'Dr. {doctor.user.get_full_name()} rejected.')
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def manage_doctors(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'hospital_admin/manage_doctors.html', {'doctors': doctors})

@user_passes_test(is_admin)
def manage_patients(request):
    patients = PatientProfile.objects.all()
    return render(request, 'hospital_admin/manage_patients.html', {'patients': patients})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, "Cannot delete admin user.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def manage_services(request):
    services = Service.objects.all()
    return render(request, 'hospital_admin/manage_services.html', {'services': services})

@user_passes_test(is_admin)
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully!')
            return redirect('manage_services')
    else:
        form = ServiceForm()
    return render(request, 'hospital_admin/add_service.html', {'form': form})

@user_passes_test(is_admin)
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('manage_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'hospital_admin/edit_service.html', {'form': form, 'service': service})

@user_passes_test(is_admin)
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, f'Service "{service.name}" deleted successfully!')
    return redirect('manage_services')
