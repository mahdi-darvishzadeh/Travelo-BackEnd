import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from website.models.users import User

@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client

@pytest.fixture
def CommonUserByEmail():
    user = User.objects.create_user(
        username = 'test-user-by-email',
        email = 'testing@gmail.com',
        password ='#correct-pass12345#'
    )
    return user

@pytest.fixture
def CommonUserByPhone():
    user = User.objects.create_user(
        username = 'test-user-by-phone',
        phone = "09010000000",
        password ="#correct-pass12345#"
    )
    return user

@pytest.mark.django_db
class TestLoginPhone():
    url = reverse('website:api-v1-accounts:login')

    def test_login_not_registered_phone_response_404(self, ApiClient , CommonUserByPhone):
        # user is not registered and wont be found (404)
        response = ApiClient.post(self.url, data={
                "phone_or_email": "09010000001",
                "password": "#false-pass12345#"
            })
        assert response.status_code == 404
        
    def test_login_not_registered_phone_response_400(self, ApiClient , CommonUserByPhone):
        # user is not registered and wont be found (404)
        response = ApiClient.post(self.url, data={
                "phone_or_email": "090100000010",
                "password": "#false-pass12345#"
            })
        assert response.status_code == 400

    def test_login_correct_phone_response_200(self, ApiClient , CommonUserByPhone):
        response = ApiClient.post(self.url, data={
                "phone_or_email": "09010000000",
                "password": "#correct-pass12345#"
            })
        assert response.status_code == 200


@pytest.mark.django_db
class TestLoginEmail():
    url = reverse('website:api-v1-accounts:login')

    def test_login_not_registered_email_response_404(self, ApiClient , CommonUserByEmail):
        # user is not registered and wont be found (404)
        response = ApiClient.post(self.url, data={
                "phone_or_email": "testing_@gmail.com",
                "password": "#failed-pass12345#"
            })
        assert response.status_code == 404

    def test_login_correct_email_response_200(self, ApiClient , CommonUserByEmail):
        response = ApiClient.post(self.url, data={
                "phone_or_email": 'testing@gmail.com',
                "password": "#correct-pass12345#"
            })
        assert response.status_code == 200