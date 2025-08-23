from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Creates a test user for debugging'

    def handle(self, *args, **options):
        # Check if test user already exists
        if User.objects.filter(username='testuser').exists():
            self.stdout.write(
                self.style.WARNING('Test user already exists')
            )
            return

        # Create test user
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password=make_password('testpass123'),
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created test user: {user.username}')
        )
        self.stdout.write('Username: testuser')
        self.stdout.write('Password: testpass123') 