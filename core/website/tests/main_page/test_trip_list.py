import pytest
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client

@pytest.mark.django_db
class TestTripList():
    url = reverse('website:main-page:list-trip')
    
    def test_business_list_response_200(self , ApiClient):
        response = ApiClient.get(self.url)
        assert response.status_code == 200