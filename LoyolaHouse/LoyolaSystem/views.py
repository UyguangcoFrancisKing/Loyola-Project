from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import EmailLevel, EmailType, Announcement
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

# Create your views here.
@never_cache
@login_required
def profiles_view(request):
    return render(request, 'system/profiles.html')

@login_required
def log_out(request):
    logout(request)
    request.session.flush()
    return redirect('users:login')

def email_view(request):
    announcements = Announcement.objects.all()
    return render(request, 'system/archive.html', {
        'announcements': announcements,
    })


def create_announcement(request):
    if request.method == 'POST':
        email_level_id = request.POST.get('email_level')
        email_type_id = request.POST.get('email_type')
        subject = request.POST.get('emailSubject')
        raw_content = request.POST.get('emailContent')

        formatted_content = convert_html_to_text(raw_content)

        if email_level_id and email_type_id and subject and raw_content:
            email_level = EmailLevel.objects.get(pk=email_level_id)
            email_type = EmailType.objects.get(pk=email_type_id)
            
            Announcement.objects.create(
                email_level=email_level,
                email_type=email_type,
                subject=subject,
                content=formatted_content 
            )
            return redirect('loyola:dashboard')

    email_levels = EmailLevel.objects.all()
    email_types = EmailType.objects.all()
    users = User.objects.all()
    
    return render(request, 'system/announcement.html', {
        'email_levels': email_levels,
        'email_types': email_types,
        'users': users,
    })


def convert_html_to_text(raw_html):
    import re
    if not raw_html:
        return '' 
    
    raw_html = raw_html.replace('&nbsp;', ' ')
    raw_html = re.sub(r'<br\s*/?>', '\n', raw_html)  # Convert <br> to \n
    text_only = strip_tags(raw_html)  # Remove remaining tags
    return text_only