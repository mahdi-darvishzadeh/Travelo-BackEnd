import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from website.models.users import User
from website.models.notification import Notification
from random import choice, randint

class Command(BaseCommand):
    help = "Populates the Notification model with random data using Faker library"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("en_US")
        
    
    
    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, help="The number of basemodel to create"
        )

    def handle(self, *args, **options):
        number = options["number"] or 50

        success_count = 0
        failed_count = 0
        users = User.objects.all()
        for i in range(number):
            try:
                notification = Notification(
                    owner=User.objects.get(id=randint(1, len(users))),
                    title=choice([1, 2, 3, 4]),
                )
                success_count += 1
                notification.save()
                print(f"{i+1}- {notification} Successfully created")
                success_count += 1
            except Exception as e:
                print(e)
                print(f"{i+1}- Failed to created")
                failed_count += 1
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(self.style.SUCCESS("Notification Faker Tasks Completed!"))
        self.stdout.write(self.style.SUCCESS(f"Total Records: {failed_count+success_count}"))
        self.stdout.write(self.style.ERROR(f"Failed Records: {failed_count}"))
        self.stdout.write(self.style.WARNING(f"Success Records: {success_count}"))
