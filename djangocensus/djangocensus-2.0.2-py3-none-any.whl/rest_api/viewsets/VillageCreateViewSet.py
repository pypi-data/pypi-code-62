from rest_framework.generics import CreateAPIView
from djangocensus.models.VillageModel import VillageModel
from djangocensus.rest_api.serializers import VillageSerializer


# Create viewset goes here.
class VillageCreateViewSet(CreateAPIView):
    serializer_class = VillageSerializer
    queryset = VillageModel

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)