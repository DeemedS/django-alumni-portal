from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Activate a user account by email"

    def add_arguments(self, parser):
        parser.add_argument('email', help='Email to activate')

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            u = User.objects.get(email=options['email'])
            u.is_active = True
            u.save()
            self.stdout.write(self.style.SUCCESS(
                f"Activated user {u.email!r}"))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                f"No user with email {options['email']}"))
