from django.core.management.base import BaseCommand
from django.db.models import Q
from faker import Faker
from website.models.chat import Chat
from website.models.users import User
from website.models.trip import Trip
from website.models.message import Message
from random import randint

class Command(BaseCommand):
    help = "Populates the message model with random data using Faker library"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("fa_IR")
        
    
    
    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, help="The number of message to create"
        )

    def handle(self, *args, **options):
        number = options["number"] or 100

        success_count = 0
        failed_count = 0
        chats = Chat.objects.all()
        for i in range(number):
            try:
                chat = Chat.objects.filter(pk=randint(1, len(chats))).first()
                if chat:
                    last_message = Message.objects.filter(chat=chat).last()
                    message = Message(
                        chat=chat,
                        content=self.fake.text(max_nb_chars=1000),
                        replay=last_message if last_message else None
                    )
                    message.save()
                    fake_boolean = self.fake.boolean()
                    if fake_boolean:
                        message.author=chat.trip.owner
                    else:
                        message.author=chat.user
                    message.save()
                    print(f"{i+1}- {message} Successfully created")
                    success_count += 1
                else:
                    print(f"{i+1}- Failed to created")
            except Exception as e:
                print(e)
                print(f"{i+1}- Failed to created")
                failed_count += 1
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(self.style.SUCCESS("Message Faker Tasks Completed!"))
        self.stdout.write(self.style.SUCCESS(f"Total Records: {failed_count+success_count}"))
        self.stdout.write(self.style.ERROR(f"Failed Records: {failed_count}"))
        self.stdout.write(self.style.WARNING(f"Success Records: {success_count}"))
