from django.core.management.base import BaseCommand
from faker import Faker
from website.models import Gallary, User
from random import choice, randint

class Command(BaseCommand):
    help = "Populates the Gallary model with random data using Faker library"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("en_US")
        self.images = [
            'static-files/gallary/1.jpeg',
            'static-files/gallary/2.jpeg',
            'static-files/gallary/3.jpeg',
            'static-files/gallary/4.jpeg',
            'static-files/gallary/5.jpeg',
            'static-files/gallary/6.jpeg',
            'static-files/gallary/7.jpeg',
            'static-files/gallary/8.jpeg',
            'static-files/gallary/9.jpeg',
            'static-files/gallary/10.jpeg',
            'static-files/gallary/11.jpeg',
            'static-files/gallary/12.jpeg',
            'static-files/gallary/13.jpeg',
        ]
    
    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--number", type=int, help="The number of gallary to create"
        )

    def handle(self, *args, **options):
        number = options["number"] or 50

        success_count = 0
        failed_count = 0
        users = User.objects.all()
        for i in range(number):
            try:
                gallary = Gallary(
                    owner=User.objects.get(id=randint(1, len(users))),
                    title=self.fake.text(max_nb_chars=120),
                    like_count=randint(1,100000),
                    dislike_count=randint(1,100000),
                    admin_verify=True,
                    description=self.fake.text(max_nb_chars=1200),
                )
                gallary.save()
                image = self.images[randint(0,12)]
                gallary.image = image
                gallary.save()
                print(f"{i+1}- {gallary} Successfully created")
                success_count += 1
            except Exception as e:
                print(e)
                print(f"{i+1}- Failed to created")
                failed_count += 1
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(self.style.SUCCESS("Gallary Faker Tasks Completed!"))
        self.stdout.write(self.style.SUCCESS(f"Total Records: {failed_count+success_count}"))
        self.stdout.write(self.style.ERROR(f"Failed Records: {failed_count}"))
        self.stdout.write(self.style.WARNING(f"Success Records: {success_count}"))
