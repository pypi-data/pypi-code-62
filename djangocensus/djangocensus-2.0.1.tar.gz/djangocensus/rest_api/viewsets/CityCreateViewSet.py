from rest_framework.generics import CreateAPIView
from djangocensus.models.CityModel import CityModel
from djangocensus.rest_api.serializers import CitySerializer


# Create viewset goes here.
class CityCreateViewSet(CreateAPIView):
    serializer_class = CitySerializer
    queryset = CityModel

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)