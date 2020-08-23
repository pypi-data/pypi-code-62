from rest_framework.generics import ListAPIView
from djangocensus.models.CityModel import CityModel
from djangocensus.rest_api.serializers import CitySerializer


# List viewset goes here.
class CityListViewSet(ListAPIView):
    serializer_class = CitySerializer
    queryset = CityModel.objects.all()