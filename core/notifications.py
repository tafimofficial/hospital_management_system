from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import Notification
from django.template.loader import render_to_string

User = get_user_model()

def send_notification_email(subject, message, recipient_list, html_message=None):
    """Send email notification from admin email"""
    try:
        if html_message:
            # Send HTML email
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.ADMIN_EMAIL,
                to=recipient_list
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
        else:
            # Send plain text email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.ADMIN_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def create_notification(user, title, message, notification_type='general', related_object_id=None, link=None):
    """Create in-app notification"""
    try:
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=related_object_id,
            link=link
        )
        return notification
    except Exception as e:
        print(f"Error creating notification: {e}")
        return None

def notify_admins(title, message, notification_type='general', related_object_id=None, link=None):
    """Send notification to all admin users"""
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        # Create in-app notification
        create_notification(admin, title, message, notification_type, related_object_id, link)
        
        # Send email if admin has email
        if admin.email:
            email_subject = f"CareConnect Admin: {title}"
            email_message = f"""
Hello {admin.get_full_name() or admin.username},

{message}

Please log in to the admin dashboard to take action.

Best regards,
CareConnect Hospital Management System
            """
            send_notification_email(
                subject=email_subject,
                message=email_message,
                recipient_list=[admin.email]
            )

def notify_user(user, title, message, notification_type='general', related_object_id=None, link=None):
    """Send notification to a specific user"""
    # Create in-app notification
    create_notification(user, title, message, notification_type, related_object_id, link)
    
    # Send email if user has email
    if user.email:
        email_subject = f"CareConnect: {title}"
        email_message = f"""
Hello {user.get_full_name() or user.username},

{message}

You can view more details by logging into your CareConnect account.

Best regards,
CareConnect Hospital Management System
        """
        send_notification_email(
            subject=email_subject,
            message=email_message,
            recipient_list=[user.email]
        )
