import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from website.models import User, Trip
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client

@pytest.fixture
def CommonTrip():
    trip = Trip.objects.create(
        pk = 10,
        like_count = '100',
        dislike_count = '4342',
    )
    return trip

@pytest.mark.django_db
class TestTripVote():
    url = reverse('website:trip:vote-trip', kwargs={"pk": 10})

    """INVALID DATA"""
    def test_create_trip_invalid_data_response_400(self, ApiClient , CommonTrip):
        # Case0: using wrong vote
        response = ApiClient.post(self.url , data = {
                "vote": "string"
            },)
        assert response.status_code == 400

        # Case1: using wrong vote
        response = ApiClient.post(self.url , data = {
                "vote": "ehgswg"
            },)
        assert response.status_code == 400

        # Case2: using wrong vote
        response = ApiClient.post(self.url , data = {
                "vote": "hrgw"
            },)
        assert response.status_code == 400

        # Case3: using wrong vote
        response = ApiClient.post(self.url , data = {
                "vote": "errhehw"
            },)
        assert response.status_code == 400
        
        # Case4: using wrong vote
        response = ApiClient.post(self.url , data = {
                "vote": "2523"
            },)
        assert response.status_code == 400

    """VALID DATA"""
    def test_vote_trip_response_201(self, ApiClient , CommonTrip):

        # Case0: standard vote 
        response = ApiClient.post(self.url , data = {
                "vote": "like"
            },)
        assert response.status_code == 200