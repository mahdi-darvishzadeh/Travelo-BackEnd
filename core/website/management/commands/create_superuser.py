from django.core.management.base import BaseCommand
from website.models import User, UserDetail
from faker import Faker
from random import choice, randint, uniform
import uuid


class Command(BaseCommand):
    help = 'Create a superuser if one does not already exist'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("en_US")
        self.images = [
            'static-files/profile/1.jpeg',
            'static-files/profile/2.jpeg',
            'static-files/profile/3.jpeg',
            'static-files/profile/4.jpeg',
            'static-files/profile/5.jpeg',
            'static-files/profile/6.jpeg',
            'static-files/profile/7.jpeg',
            'static-files/profile/8.jpeg',
            'static-files/profile/9.jpeg',
            'static-files/profile/10.jpeg',
            'static-files/profile/11.jpeg',
            'static-files/profile/12.jpeg',
            'static-files/profile/13.jpeg',
            'static-files/profile/14.jpeg',
        ]
    
    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                phone='123456789',
                password='admin'
            )
            
            userDetail = UserDetail.objects.get(user=user)
            
            userDetail.gender = choice(["male", "Female"])
            if userDetail.gender == "male":
                first_name = self.fake.first_name_male()
            else:
                first_name = self.fake.first_name_female()
                
            userDetail.first_name = first_name
            userDetail.last_name = self.fake.last_name()
            userDetail.education = choice(["Computer Engineering", "electrical engineering", "mechanical engineering", "industrial engineering", "chemical engineering", "Petroleum engineering", "Materials Engineering", "Accounting", "Physics", "Humanities"])
            userDetail.career = self.fake.job()
            userDetail.living_in = self.fake.city()
            userDetail.birthdate = self.fake.date()
            userDetail.personality_type = choice(["Normal", "Introverted", "extroverted"])
            userDetail.workout = choice(["Bodybuilding", "Soccer", "Volleyball", "gymnastics", "tennis"])
            
            unique_numbers = []
            while len(unique_numbers) < 10:
                unique_numbers.append(self.fake.unique.random_number(digits=10))
                
            userDetail.marital_status = choice(["married", "Single"])
            userDetail.description = self.fake.paragraph(nb_sentences=5)
            userDetail.phone_number = "+98912 3456 789"
            userDetail.telegram = f"telegram-{unique_numbers[2]}"
            userDetail.instagram = f"instagram-{unique_numbers[4]}"
            userDetail.rate = float("%.2f" % uniform(0,5))
            userDetail.trips_count = randint(0, 100)                 
            userDetail.save()
            image = self.images[randint(0,13)]
            userDetail.image = image
            userDetail.save()
            self.stdout.write(self.style.SUCCESS('Successfully created superuser.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
        