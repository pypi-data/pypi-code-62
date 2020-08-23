from rest_framework.generics import RetrieveAPIView
from djangocensus.models.CityModel import CityModel
from djangocensus.rest_api.serializers import CitySerializer


# Detail viewset goes here.
class CityDetailViewSet(RetrieveAPIView):
    serializer_class = CitySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = CityModel