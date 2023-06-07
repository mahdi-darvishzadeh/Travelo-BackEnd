import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from website.models.users import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client

@pytest.fixture
def CommonUserByEmail():
    user = User.objects.create_user(
        pk = 2,
        username = 'test-admin',
        email = 'testing@gmail.com',
        password ='#correct-pass12345#'
    )
    return user


@pytest.mark.django_db
class TestCreateTrip():
    url = reverse('website:trip:create-trip')

    """INVALID DATA"""
    def test_create_trip_invalid_data_response_400(self, ApiClient , CommonUserByEmail):
        refresh = RefreshToken.for_user(User.objects.get(pk = '2'))
        # Case0: using wrong moving_day
        response = ApiClient.post(self.url , data = {
                "owner" : "2",
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "fd-ddv-2",
                "Transportstion" : "سواری",
                "price" : "240000",
                "description" : "test-description",
            },
            **{'HTTP_AUTHORIZATION' : f"Bearer {str(refresh.access_token)}"})
        assert response.status_code == 400

        # Case1: using wrong moving_day
        response = ApiClient.post(self.url , data = {
                "owner" : "2",
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "fhb-06-2",
                "Transportstion" : "سواری",
                "price" : "250000",
                "description" : "test-description",
            },
            **{'HTTP_AUTHORIZATION' : f"Bearer {str(refresh.access_token)}"})
        assert response.status_code == 400

        # Case2: using wrong price
        response = ApiClient.post(self.url , data = {
                "owner" : "2",
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "2023-06-05",
                "Transportstion" : "سواری",
                "price" : "ergea",
                "description" : "test-description",
            },
            **{'HTTP_AUTHORIZATION' : f"Bearer {str(refresh.access_token)}"})
        assert response.status_code == 400

        # Case3: using wrong moving_day
        response = ApiClient.post(self.url , data = {
                "owner" : "2",
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "20f-06-02",
                "Transportstion" : "سواری",
                "price" : "240000",
                "description" : "test-description",
            },
            **{'HTTP_AUTHORIZATION' : f"Bearer {str(refresh.access_token)}"})
        assert response.status_code == 400
        
        # Case4: using wrong owner
        response = ApiClient.post(self.url , data = {
                "owner" : "700",
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "2023-12-02",
                "Transportstion" : "سواری",
                "price" : "240000",
                "description" : "test-description",
            },
            **{'HTTP_AUTHORIZATION' : f"Bearer {str(refresh.access_token)}"})
        assert response.status_code == 400

    """UNAUTHORIZED trip"""
    def test_create_trip_unauthorized_response_401(self , ApiClient , CommonUserByEmail):

        # Case0: without using access_token for create_trip_unauthorized_response
        response = ApiClient.post(self.url , data = {
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "2023-05-23",
                "Transportstion" : "سواری",
                "price" : "240000",
                "description" : "test-description",
            })
        assert response.status_code == 401

    """VALID DATA"""
    def test_create_trip_response_201(self, ApiClient , CommonUserByEmail):
        refresh = RefreshToken.for_user(User.objects.get(pk = '2'))

        # Case0: standard moving_day and price 
        response = ApiClient.post(self.url , data = {
                "owner" : "2",
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "2024-10-12",
                "Transportstion" : "سواری",
                "price" : "240000",
                "description" : "test-description",
            },
            **{'HTTP_AUTHORIZATION' : f"Bearer {str(refresh.access_token)}"})
        assert response.status_code == 201