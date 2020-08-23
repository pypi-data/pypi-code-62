from rest_framework.generics import CreateAPIView
from djangocensus.models.DistrictModel import DistrictModel
from djangocensus.rest_api.serializers import DistrictSerializer


# Create viewset goes here.
class DistrictCreateViewSet(CreateAPIView):
    serializer_class = DistrictSerializer
    queryset = DistrictModel

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)