from rest_framework.generics import CreateAPIView
from djangocensus.models.StateModel import StateModel
from djangocensus.rest_api.serializers import StateSerializer


# Create viewset goes here.
class StateCreateViewSet(CreateAPIView):
    serializer_class = StateSerializer
    queryset = StateModel

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)