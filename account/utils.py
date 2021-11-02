from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def new_user_notification(request, user):
    subject = 'New Member for Taiwan New Yorker'
    # message = user.get_full_name() + ' age: ' + str(user.age())
    html_message = render_to_string('account/new_user_notification.html', {'user': user})
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['raymondcyang0219@gmail.com',]
    send_mail(subject, '', email_from, recipient_list, html_message=html_message,)
    return
