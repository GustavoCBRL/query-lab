from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Send a test email using the current Django email settings."

    def add_arguments(self, parser):
        parser.add_argument("recipient", help="Destination email address.")

    def handle(self, *args, **options):
        recipient = options["recipient"]

        if not settings.DEFAULT_FROM_EMAIL:
            raise CommandError("DEFAULT_FROM_EMAIL is empty.")

        sent_count = send_mail(
            subject="SQL Study Hub email test",
            message="This is a test email sent from the Railway deployment.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

        if sent_count != 1:
            raise CommandError("Email backend did not confirm delivery.")

        self.stdout.write(self.style.SUCCESS(f"Test email sent to {recipient}."))