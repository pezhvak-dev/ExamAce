from django.core.mail import send_mail


def send_created_weblog_email_to_news_letter(emails: list, *args):
    subject = f'یک وبلاگ جدید!'
    message = f'''
یک وبلاگ جدید در وبسایت قرار داده شد. جهت دسترسی سریع، از طریف لینک زیر به صفحه جزئیات آن بروید.
{args[0]}
'''
    from_email = 'django <baniadampouya2000@gmail.com>'

    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=emails,
              fail_silently=False)