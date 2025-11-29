from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification

@login_required
def get_notifications(request):
    """Get user's notifications"""
    notifications = request.user.notifications.all()[:10]  # Latest 10
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    notifications_data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'is_read': n.is_read,
        'created_at': n.created_at.strftime('%b %d, %Y %I:%M %p'),
        'link': n.link or '#'
    } for n in notifications]
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})

@login_required
@require_POST
def mark_all_read(request):
    """Mark all notifications as read"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

@login_required
def all_notifications(request):
    """View all notifications page"""
    notifications = request.user.notifications.all()
    return render(request, 'core/notifications.html', {'notifications': notifications})
