from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import EmailLevel, EmailType, Announcement, ViberContact
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import requests

# Create your views here.
@never_cache
@login_required
def profiles_view(request):
    accounts = User.objects.all()
    contacts = ViberContact.objects.all()
    return render(request, 'system/profiles.html', {
        'accounts': accounts,
        'contacts': contacts,
    })

@login_required
def log_out(request):
    logout(request)
    request.session.flush()
    return redirect('users:login')

@login_required
def email_view(request):
    announcements = Announcement.objects.all()
    return render(request, 'system/archive.html', {
        'announcements': announcements,
    })

@login_required
def create_announcement(request):
    if request.method == 'POST':
        email_level_id = request.POST.get('email_level')
        email_type_id = request.POST.get('email_type')
        subject = request.POST.get('emailSubject')
        raw_content = request.POST.get('emailContent')

        formatted_content = convert_html_to_text(raw_content)
        viber_contacts = ViberContact.objects.filter(user=request.user)

        if email_level_id and email_type_id and subject and raw_content:
            email_level = EmailLevel.objects.get(pk=email_level_id)
            email_type = EmailType.objects.get(pk=email_type_id)
            for contact in viber_contacts:
                sendNotif(contact.viber_id, formatted_content)
            
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

def sendNotif (receiver_id ,message):
    viber_api_url = 'https://chatapi.viber.com/pa/send_message'
    headers = {
        'X-Viber-Auth-Token': 'YOUR_VIBER_BOT_AUTH_TOKEN',  # Replace with your bot token
        'Content-Type': 'application/json'
    }
    payload = {
        "receiver": receiver_id,
        "min_api_version": 1,
        "sender": {
            "name": "Loyola Bot",
            "avatar": "https://example.com/avatar.jpg"  # Optional
        },
        "type": "text",
        "text": message
    }
    response = requests.post(viber_api_url, json=payload, headers=headers)
    return response.status_code, response.json()

def convert_html_to_text(raw_html):
    import re
    if not raw_html:
        return '' 
    
    raw_html = raw_html.replace('&nbsp;', ' ')
    raw_html = re.sub(r'<br\s*/?>', '\n', raw_html)  # Convert <br> to \n
    text_only = strip_tags(raw_html)  # Remove remaining tags
    return text_only