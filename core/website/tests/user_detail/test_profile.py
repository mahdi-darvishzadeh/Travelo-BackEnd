import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from website.models.users import User
from website.models.profile import UserDetail


@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client

@pytest.fixture
def CommonUser():
    user = User.objects.create_user(
        username = 'testing-username-field',
        phone = '09010000000',
        password ='#correct-pass12345#'
    )
    user_profile = UserDetail.objects.get(user=user)
    return user_profile

@pytest.mark.django_db
class TestProfile():
    url = reverse(
        'website:user-detail:profile', kwargs={
        "username": "testing-username-field"
        })
    
    def test_my_profile_detail_response_200(self, ApiClient, CommonUser):
        response = ApiClient.get(self.url)
        content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert 'phone' in content
        assert 'email' in content
        assert 'first_name' in content
        assert 'last_name' in content
        assert 'education' in content
        assert 'job' in content
        assert 'gender' in content
        assert 'marital_status' in content
        assert 'age' in content
        assert 'city' in content
        assert 'completion_percentage' in content

