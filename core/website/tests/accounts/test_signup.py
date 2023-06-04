import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from website.models.users import User

@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client


@pytest.mark.django_db
class TestSignupByEmail():
    url = reverse('website:api-v1-accounts:signup')

    """INVALID EMAIL"""
    def test_signup_invalid_email_response_400(self, ApiClient):
        # testing all the possible phone_or_email inputs
        # which are meant to be email
        
        # Case0: using whitespaces in phone_or_email field
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testing whitespace@gmail.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case1: no @ in input
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingwhitespacegmail.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case2: no . in input
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingwhitespace@gmailcom",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case3: no "com" in input
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingwhitespacegmail.",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400
        
        # Case4: more than one @
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingwhitespace@@gmail.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case4: more than one .
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingwhitespace@gmai.l.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case5: more than one .
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingwhitespace@gmai.l.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case6: does not contain first part
        response = ApiClient.post(self.url, data={
            "phone_or_email": "@gmail.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case7: does not contain mid part
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingmail@.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case8: does not contain last part
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testingmail@gmail.",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

    """VALID EMAIL"""
    def test_signup_valid_email_response_201(self, ApiClient):
        # testing all the possible phone_or_email inputs
        # which are meant to be email

        # Case0: standard gmail address
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testing@gmail.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 201
        # check if the email field is not empty
        user = User.objects.filter(email="testing@gmail.com")
        assert user.exists() == True

        # Case1: standard outlook address
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testing@outlook.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 201
        # check if the email field is not empty
        user = User.objects.filter(email="testing@outlook.com")
        assert user.exists() == True

        # Case2: standard yahoo address
        response = ApiClient.post(self.url, data={
            "phone_or_email": "testing@yahoo.com",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 201
        # check if the email field is not empty
        user = User.objects.filter(email="testing@yahoo.com")
        assert user.exists() == True


@pytest.mark.django_db
class TestSignupByPhone():
    url = reverse('website:api-v1-accounts:signup')

    """INVALID PHONE"""
    def test_signup_invalid_phone_response_400(self, ApiClient):
        # testing all the possible phone_or_email inputs
        # which are meant to be phone

        # Case1: using none number char in phone_or_email field
        response = ApiClient.post(self.url, data={
            "phone_or_email": "0t9e2s3t5i7ng",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case2: using less than 11 char in phone_or_email field
        response = ApiClient.post(self.url, data={
            "phone_or_email": "0123456789",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

        # Case2: using more than 11 char in phone_or_email field
        response = ApiClient.post(self.url, data={
            "phone_or_email": "01234567890123",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400
        
        # Case3: using more than 11 char in phone number start with 09
        response = ApiClient.post(self.url, data={
            "phone_or_email": "093900596099",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400
        
        # Case4 : using string in phone field
        response = ApiClient.post(self.url, data={
            "phone_or_email": "aaaaaaaaaaa",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 400

    """VALID PHONE"""
    def test_signup_valid_phone_response_201(self, ApiClient):
        # testing all the possible phone_or_email inputs
        # which are meant to be phone
        
        # Case0: standard phone number
        response = ApiClient.post(self.url, data={
            "phone_or_email": "09121231234",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 201
        # check if user is available with the given phone
        user = User.objects.filter(phone="09121231234")
        assert user.exists() == True

        # Case1: phone number which starts with +98
        response = ApiClient.post(self.url, data={
            "phone_or_email": "+989121231234",
            "first_name": "first-name",
            "last_name": "last-name",
            "password": "#normal-pass12345#",
            "password2": "#normal-pass12345#"
        })
        assert response.status_code == 201
        # check if user is available with the given phone
        user = User.objects.filter(phone="+989121231234")
        assert user.exists() == True
