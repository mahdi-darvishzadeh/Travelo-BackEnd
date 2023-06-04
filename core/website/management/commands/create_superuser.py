from django.core.management.base import BaseCommand
from website.models import User , UserDetail
import random
from faker import Faker


class Command(BaseCommand):
    help = 'Create a superuser if one does not already exist'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker("fa_IR")
    
    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                phone='123456789',
                password='admin'
            )
            for i in range(5) :
                try:
                    user = User.objects.create_user(username=f'username{str(i + 1)}' , password="fake@1234",
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
                    userDetail.birthdate = self.fake.date()
                    unique_numbers = []
                    while len(unique_numbers) < 10:
                        unique_numbers.append(self.fake.unique.random_number(digits=10))
                    userDetail.marital_status = random.choice(["متاهل", "مجرد"])
                    userDetail.favorite = self.fake.paragraph(nb_sentences=5)
                    userDetail.telegram = unique_numbers[2]
                    userDetail.instagram = unique_numbers[4]
                    userDetail.save()
                except Exception as e:
                    print(e)
                    print("Username has already been taken!")

            self.stdout.write(self.style.SUCCESS('Successfully created superuser.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
        