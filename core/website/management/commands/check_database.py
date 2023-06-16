import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from faker import Faker
import random
from website.models import User
from website.models import UserDetail
from random import randint, uniform, random, choice
import uuid


class Command(BaseCommand):
    help = 'check if database is online to proceed'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("fa_IR")
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
    
    def handle(self, *args, **kwargs):
        ''' generate 50 fake user and user profile'''
        for _ in range(50) :
            uuid_tmp = str(uuid.uuid4())
            x = uuid_tmp.split("-")
            id = choice(x)
            try:
                user = User.objects.create_user(username=f"travelo-{id}" , password="fake@1234",
                                                phone=self.fake.phone_number() , email=self.fake.email())
                userDetail = UserDetail.objects.get(user=user)
                userDetail.gender = choice(["مرد", "زن"])
                if userDetail.gender == "male" or "مرد":
                    first_name = self.fake.first_name_male()
                else:
                    first_name = self.fake.first_name_female()
                userDetail.first_name = first_name
                userDetail.last_name = self.fake.last_name()
                userDetail.education = choice(["مهندسی کامپیوتر", "مهدسی برق", "مهندسی مکانیک", "مهندسی ضنایع", "مهندسی شیمی", "مهندسی نفت", "مهندسی مواد", "حسایداری", "فیزیک", "علوم انسانی"])
                userDetail.career = self.fake.job()
                userDetail.living_in = self.fake.city()
                userDetail.birthdate = self.fake.date()
                userDetail.personality_type = choice(["معمولی", "درونگرا", "برونگرا"])
                userDetail.workout = choice(["بدنسازی", "فوتبال", "والیبال", "ژیمناستیک", "تنیس"])
                unique_numbers = []
                while len(unique_numbers) < 10:
                    unique_numbers.append(self.fake.unique.random_number(digits=10))
                userDetail.marital_status = choice(["متاهل", "مجرد"])
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
        