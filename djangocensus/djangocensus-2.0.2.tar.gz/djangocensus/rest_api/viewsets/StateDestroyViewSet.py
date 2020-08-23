from rest_framework.generics import DestroyAPIView
from djangocensus.models.StateModel import StateModel
from djangocensus.rest_api.serializers import StateSerializer


# Create viewset goes here.
class StateDestroyViewSet(DestroyAPIView):
    serializer_class = StateSerializer
    queryset = StateModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"