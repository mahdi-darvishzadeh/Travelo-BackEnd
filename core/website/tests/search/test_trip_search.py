import pytest
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client

@pytest.mark.django_db
class TestTripSearch():
    url = reverse('website:search:trip')
    
    def test_trip_search_response_200(self , ApiClient):
        response = ApiClient.get(self.url,data = {
                "owner" : "2",
                "country" : "ایران",
                "from_city" : "تهران",
                "to_city" : "سمنان",
                "moving_day" : "2024-10-12",
                "Transportstion" : "سواری",
                "price" : "240000",
                "description" : "test-description",
            },)
        assert response.status_code == 200