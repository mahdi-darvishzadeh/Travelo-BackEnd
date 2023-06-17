from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from website.models import Trip, User
from random import choice, randint, uniform
import json

class Command(BaseCommand):
    help = "Populates the Trip model with random data using Faker library"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("en_US")
        with open('assets/cities.json') as read_file:
            self.r = read_file.read()
            self.cities = json.loads(self.r)
    
    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, help="The number of trip to create"
        )

    def handle(self, *args, **options):
        number = options["number"] or 50

        success_count = 0
        failed_count = 0
        users = User.objects.all()
        for i in range(number):
            try:
                trip = Trip(
                    owner=User.objects.get(id=randint(1, len(users))),
                    country="Iran",
                    from_city=choice(self.cities[randint(0, len(self.cities))]['sub']),
                    to_city=choice(self.cities[randint(0, len(self.cities))]['sub']),
                    moving_day=timezone.now(),
                    day_to=timezone.now(),
                    appear_in_search=True,
                    Transportstion=choice(["Riding","Minibus","Van","minion","Bus","Engine"]),
                    price=randint(50000,500000),
                    like_count=randint(1,100000),
                    dislike_count=randint(1,100000),
                    rate = float("%.2f" % uniform(0,5)),
                    description=self.fake.text(max_nb_chars=1200),
                )
                trip.save()
                print(f"{i+1}- {trip} Successfully created")
                success_count += 1
            except Exception as e:
                print(e)
                print(f"{i+1}- Failed to created")
                failed_count += 1
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(self.style.SUCCESS("Trip Faker Tasks Completed!"))
        self.stdout.write(self.style.SUCCESS(f"Total Records: {failed_count+success_count}"))
        self.stdout.write(self.style.ERROR(f"Failed Records: {failed_count}"))
        self.stdout.write(self.style.WARNING(f"Success Records: {success_count}"))
