from rest_framework.generics import CreateAPIView
from djangocensus.models.ContinentModel import ContinentModel
from djangocensus.rest_api.serializers import ContinentSerializer


# Create viewset goes here.
class ContinentCreateViewSet(CreateAPIView):
    serializer_class = ContinentSerializer
    queryset = ContinentModel

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)