from rest_framework.generics import DestroyAPIView
from djangocensus.models.CityModel import CityModel
from djangocensus.rest_api.serializers import CitySerializer


# Create viewset goes here.
class CityDestroyViewSet(DestroyAPIView):
    serializer_class = CitySerializer
    queryset = CityModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"