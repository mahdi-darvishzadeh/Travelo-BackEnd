import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from faker import Faker
import random
from website.models import User
from website.models import UserDetail


class Command(BaseCommand):
    help = 'check if database is online to proceed'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("fa_IR")
    
    def handle(self, *args, **kwargs):
        ''' generate 50 fake user and user profile'''
        for _ in range(50) :
            try:
                user = User.objects.create_user(username=self.fake.user_name() , password="fake@1234",
                                                phone = self.fake.phone_number() , email = self.fake.email())
                userDetail = UserDetail.objects.get(user=user)
                userDetail.gender = random.choice(["مرد", "زن"])
                if userDetail.gender == "male":
                    first_name = self.fake.first_name_male()
                else:
                    first_name = self.fake.first_name_female()
                last_name = self.fake.last_name()
                userDetail.fullname = first_name + ' ' + last_name
                userDetail.education = self.fake.text(max_nb_chars=10)
                userDetail.job = self.fake.job()
                userDetail.city = self.fake.city()
                userDetail.province = self.fake.city()
                userDetail.post_code = self.fake.postcode()
                userDetail.birthdate = self.fake.date()
                unique_numbers = []
                while len(unique_numbers) < 10:
                    unique_numbers.append(self.fake.unique.random_number(digits=10))
                userDetail.veterinary_number = unique_numbers[0]
                userDetail.marital_status = random.choice(["متاهل", "مجرد"])
                userDetail.national_code = unique_numbers[1]
                userDetail.favorite = self.fake.paragraph(nb_sentences=5)
                userDetail.telephone = self.fake.unique.random_number(digits=10)
                userDetail.telegram = unique_numbers[2]
                userDetail.twitter = unique_numbers[3]
                userDetail.instagram = unique_numbers[4]
                userDetail.tiktok = unique_numbers[5]
                userDetail.bale = unique_numbers[6]
                userDetail.rubika = unique_numbers[7]
                userDetail.gap = unique_numbers[8]
                userDetail.website = self.fake.url()
                userDetail.save()
            except:
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
        