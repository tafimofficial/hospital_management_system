from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from blood_bank.models import BloodInventory, BloodRequest, BloodDonor
from doctor.models import DoctorProfile, Appointment
from core.notifications import notify_user

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def manage_blood_bank(request):
    inventory = BloodInventory.objects.all().order_by('blood_group')
    requests = BloodRequest.objects.all().order_by('-request_date')
    pending_donors = BloodDonor.objects.filter(status='pending').order_by('-id')
    return render(request, 'hospital_admin/blood_bank_dashboard.html', {
        'inventory': inventory,
        'requests': requests,
        'pending_donors': pending_donors
    })

@user_passes_test(is_admin)
def manage_blood_donor(request, pk):
    if request.method == 'POST':
        donor = get_object_or_404(BloodDonor, pk=pk)
        action = request.POST.get('action')
        
        if action == 'approve':
            donor.status = 'approved'
            messages.success(request, f'Donor {donor.name} approved.')
        elif action == 'reject':
            donor.status = 'rejected'
            messages.warning(request, f'Donor {donor.name} rejected.')
            
        donor.save()
    return redirect('manage_blood_bank')

@user_passes_test(is_admin)
def update_blood_inventory(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(BloodInventory, pk=pk)
        bags = int(request.POST.get('bags', 0))
        item.bags_available = bags
        item.save()
        messages.success(request, f'Updated {item.blood_group} inventory.')
    return redirect('manage_blood_bank')

@user_passes_test(is_admin)
def manage_blood_request(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(BloodRequest, pk=pk)
        action = request.POST.get('action')
        
        if action == 'approve':
            # Check inventory
            inventory_item = BloodInventory.objects.filter(blood_group=req.blood_group).first()
            
            if inventory_item:
                available = inventory_item.bags_available
                requested = req.units_needed
                
                if available >= requested:
                    # Full approval
                    inventory_item.bags_available -= requested
                    inventory_item.save()
                    
                    req.status = 'approved'
                    req.units_approved = requested
                    req.admin_comment = f'Request fully approved. {requested} units provided.'
                    req.save()
                    
                    # Notify patient
                    if req.user:
                        notify_user(
                            user=req.user,
                            title='Blood Request Approved',
                            message=f'Your request for {requested} units of {req.blood_group} blood has been approved.',
                            notification_type='blood_request',
                            related_object_id=req.id
                        )
                    
                    messages.success(request, f'Request approved. {requested} units deducted from {req.blood_group} inventory.')
                    
                elif available > 0:
                    # Partial approval
                    inventory_item.bags_available = 0
                    inventory_item.save()
                    
                    req.status = 'approved'
                    req.units_approved = available
                    req.admin_comment = f'We only have {available} units available. {available} units provided out of {requested} requested.'
                    req.save()
                    
                    # Notify patient
                    if req.user:
                        notify_user(
                            user=req.user,
                            title='Blood Request Partially Approved',
                            message=f'Your request for {requested} units of {req.blood_group} blood has been partially approved. We are providing {available} units.',
                            notification_type='blood_request',
                            related_object_id=req.id
                        )
                    
                    messages.warning(request, f'Partial approval: Only {available} units available. {available} units deducted from {req.blood_group} inventory.')
                    
                else:
                    # No inventory
                    messages.error(request, f'No {req.blood_group} inventory available. Cannot approve request.')
            else:
                messages.error(request, f'Blood group {req.blood_group} not found in inventory.')
                
        elif action == 'reject':
            req.status = 'rejected'
            req.admin_comment = 'Request rejected by admin.'
            req.save()
            
            # Notify patient
            if req.user:
                notify_user(
                    user=req.user,
                    title='Blood Request Rejected',
                    message=f'Your request for {req.units_needed} units of {req.blood_group} blood has been rejected.',
                    notification_type='blood_request',
                    related_object_id=req.id
                )
            
            messages.warning(request, 'Request rejected.')
    return redirect('manage_blood_bank')
