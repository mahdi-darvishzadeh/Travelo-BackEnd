from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from website.models.users import User
from website.models.trip import Trip
from website.models.chat import Chat
from random import choice, randint

class Command(BaseCommand):
    help = "Populates the chat model with random data using Faker library"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("fa_IR")
        
    
    
    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, help="The number of chat to create"
        )

    def handle(self, *args, **options):
        number = options["number"] or 50

        success_count = 0
        failed_count = 0
        users = User.objects.all()
        trips = Trip.objects.all()
        for i in range(number):
            try:
                chat, created = Chat.objects.get_or_create(
                    user=User.objects.get(id=randint(1, len(users))),
                    trip=Trip.objects.get(id=randint(1, len(trips))),
                )
                print(f"{i+1}- {chat} Successfully created")
                success_count += 1
            except Exception as e:
                print(e)
                print(f"{i+1}- Failed to created")
                failed_count += 1
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(self.style.SUCCESS("Chat Faker Tasks Completed!"))
        self.stdout.write(self.style.SUCCESS(f"Total Records: {failed_count+success_count}"))
        self.stdout.write(self.style.ERROR(f"Failed Records: {failed_count}"))
        self.stdout.write(self.style.WARNING(f"Success Records: {success_count}"))
