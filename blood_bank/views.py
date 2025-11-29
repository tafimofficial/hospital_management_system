from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BloodInventory, BloodDonor, BloodRequest
from .forms import BloodDonorForm, BloodRequestForm
from django.contrib.auth.decorators import login_required
from core.notifications import notify_admins

def blood_bank_home(request):
    inventory = BloodInventory.objects.all()
    # Ensure all blood groups exist in inventory
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    for bg in blood_groups:
        BloodInventory.objects.get_or_create(blood_group=bg)
    
    inventory = BloodInventory.objects.all().order_by('blood_group')
    return render(request, 'blood_bank/home.html', {'inventory': inventory})

def register_donor(request):
    if request.method == 'POST':
        form = BloodDonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            if request.user.is_authenticated:
                donor.user = request.user
            donor.save()
            messages.success(request, 'Thank you for registering as a blood donor! You are now listed.')
            return redirect('blood_bank_home')
    else:
        form = BloodDonorForm()
    return render(request, 'blood_bank/register_donor.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def request_blood(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.save()
            
            # Send notification to admins
            notify_admins(
                title=f'New Blood Request: {blood_request.blood_group}',
                message=f'{blood_request.patient_name} has requested {blood_request.units_needed} units of {blood_request.blood_group} blood. Reason: {blood_request.reason}',
                notification_type='blood_request',
                related_object_id=blood_request.id,
                link='/hospital_admin/blood-bank/'
            )
            
            messages.success(request, 'Your blood request has been submitted. We will contact you shortly.')
            return redirect('blood_bank_home')
    else:
        # Pre-fill patient name if user has a profile
        initial_data = {'patient_name': request.user.get_full_name()}
        form = BloodRequestForm(initial=initial_data)
    return render(request, 'blood_bank/request_blood.html', {'form': form})

def find_donors(request):
    blood_group = request.GET.get('blood_group')
    donors = BloodDonor.objects.filter(is_anonymous=False, status='approved')
    
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    
    return render(request, 'blood_bank/find_donors.html', {
        'donors': donors,
        'current_filter': blood_group
    })
