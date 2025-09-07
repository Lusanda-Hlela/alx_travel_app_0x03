from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Send a test email to verify SMTP settings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            type=str,
            help="Recipient email address",
            default="sanda.normal@gmail.com",  # change default if you want
        )

    def handle(self, *args, **options):
        recipient = options["to"]
        try:
            sent = send_mail(
                subject="Django Test Email",
                message="This is a test email sent via Django management command.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            if sent:
                self.stdout.write(
                    self.style.SUCCESS(f"Email successfully sent to {recipient}")
                )
            else:
                self.stdout.write(self.style.ERROR("Email could not be sent."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
