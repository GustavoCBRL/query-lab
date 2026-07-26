import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.exceptions import ImproperlyConfigured
    
    
class ResendEmailBackend(BaseEmailBackend):
        def __init__(self, fail_silently=False, **kwargs):
            super().__init__(fail_silently=fail_silently, **kwargs)
            api_key = getattr(settings, "RESEND_API_KEY", "")
            if not api_key:
                if not self.fail_silently:
                    raise ImproperlyConfigured("RESEND_API_KEY is not configured.")
            else:
                resend.api_key = api_key
    
        def send_messages(self, email_messages):
            if not email_messages:
                return 0
    
            sent_count = 0
            for message in email_messages:
                try:
                    from_email = message.from_email or getattr(
                        settings, "DEFAULT_FROM_EMAIL", "onboarding@resend.dev"
                    )
                    
                    # Se for o e-mail de exemplo padrão do Django, ajusta para o remetente gratuito do Resend
                    if "example.com" in from_email or not from_email:
                        from_email = "onboarding@resend.dev"
    
                    payload = {
                        "from": from_email,
                        "to": message.to,
                        "subject": message.subject,
                    }
    
                    # Suporte para e-mails HTML e texto puro
                    html_content = None
                    if hasattr(message, "alternatives"):
                        for content, mimetype in message.alternatives:
                            if mimetype == "text/html":
                                html_content = content
                                break
    
                    if html_content:
                        payload["html"] = html_content
                        payload["text"] = message.body
                    else:
                        payload["text"] = message.body
    
                    if message.cc:
                        payload["cc"] = message.cc
                    if message.bcc:
                        payload["bcc"] = message.bcc
                    if message.reply_to:
                        payload["reply_to"] = message.reply_to
    
                    response = resend.Emails.send(payload)
                    if response:
                        sent_count += 1
                except Exception as e:
                    if not self.fail_silently:
                        raise e
    
            return sent_count
