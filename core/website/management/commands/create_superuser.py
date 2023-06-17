from django.core.management.base import BaseCommand
from website.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'Create a superuser if one does not already exist'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("en_US")
    
    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                phone='123456789',
                password='admin'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created superuser.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
        