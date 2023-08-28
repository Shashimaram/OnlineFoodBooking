from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
def detectUser(user):
    redirectUrl = None
    if user.role == 1:
        redirectUrl = 'accounts:vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'accounts:custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def send_verification_email(request, user, mail_subject, email_subject):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site =  get_current_site(request)# this need to be changed when app is in production
    mail_subject ="Please activate your account"
    message =render_to_string('accounts/email/account_verification_email.html',{
        'user': user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),

    })
    to_email= user.email
    mail =EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()


def send_password_reset_email(request, user,mail_subject,email_template):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site =  get_current_site(request)# this need to be changed when app is in production
    mail_subject ="Reset Your password"
    message =render_to_string(email_template,{
        'user': user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),

    })
    to_email= user.email
    mail =EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()


def send_notification(mail_subject,mail_template,context):
    """This is the Dynamic way of sending notification, we need to change the mail_template, mail_subject and context"""
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject,message, from_email, to=[to_email])
    mail.send()
