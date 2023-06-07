import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from website.models import Trip
from website.models.profile import UserDetail
import mock
from rest_framework.response import Response
from website.api.v1.main_page.serializers import TripSerializerRetrieve
from django.shortcuts import get_object_or_404
from website.api.v1.main_page import views

@pytest.fixture
def ApiClient():
    # anonymous user
    client = APIClient()
    return client

@pytest.fixture
def CommonBusiness():
    trip = Trip.objects.create(
        pk = 10,
        appear_in_search=False,
    )
    return trip

@pytest.mark.django_db
class TestTripRetrieve():
    url = reverse(
            'website:main-page:retrieve-trip', kwargs={
            "pk": 10,
            })
    def test_trip_retrieve_response_200(self, ApiClient,CommonBusiness):
        with mock.patch('website.api.v1.main_page.views.TripViewSet.retrieve') as mock_trip_retrieve:
            trip = get_object_or_404(Trip, pk=CommonBusiness.pk, appear_in_search=False)
            serializer = TripSerializerRetrieve(trip)
            mock_trip_retrieve.return_value = Response(serializer.data)

            response = ApiClient.get(self.url)
            assert response.status_code == 200

