import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from faker import Faker
import random
from website.models import User
from website.models import UserDetail
from random import randint, uniform, random, choice


class Command(BaseCommand):
    help = 'check if database is online to proceed'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("fa_IR")
        self.images = [
            'static-files/faker/1.jpeg',
            'static-files/faker/2.jpeg',
            'static-files/faker/3.jpeg',
            'static-files/faker/4.jpeg',
            'static-files/faker/5.jpeg',
        ]
    
    def handle(self, *args, **kwargs):
        ''' generate 50 fake user and user profile'''
        for _ in range(50) :
            try:
                user = User.objects.create_user(username=self.fake.user_name() , password="fake@1234",
                                                phone = self.fake.phone_number() , email = self.fake.email())
                userDetail = UserDetail.objects.get(user=user)
                userDetail.gender = choice(["مرد", "زن"])
                if userDetail.gender == "male" or "مرد":
                    first_name = self.fake.first_name_male()
                else:
                    first_name = self.fake.first_name_female()
                userDetail.first_name = first_name
                userDetail.last_name = self.fake.last_name()
                userDetail.education = self.fake.text(max_nb_chars=10)
                userDetail.job = self.fake.job()
                userDetail.city = self.fake.city()
                userDetail.birthdate = self.fake.date()
                unique_numbers = []
                while len(unique_numbers) < 10:
                    unique_numbers.append(self.fake.unique.random_number(digits=10))
                userDetail.marital_status = choice(["متاهل", "مجرد"])
                userDetail.description = self.fake.paragraph(nb_sentences=5)
                userDetail.phone_number = self.fake.unique.random_number(digits=15)
                userDetail.telegram = unique_numbers[2]
                userDetail.instagram = unique_numbers[4]
                userDetail.rate = float("%.2f" % uniform(0,5))
                userDetail.trips_count = randint(0, 100)
                userDetail.save()
                image = self.images[randint(0,4)]
                userDetail.image = image
                userDetail.save()
            except Exception as e:
                print(e)
                print("Username has already been taken!")
        print("Start checking for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                print('Database unavailable, waiting 1 second...')
                time.sleep(1)

        print("Database Available!")
        