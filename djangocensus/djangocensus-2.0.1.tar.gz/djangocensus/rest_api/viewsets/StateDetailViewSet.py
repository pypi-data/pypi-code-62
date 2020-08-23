from rest_framework.generics import RetrieveAPIView
from djangocensus.models.StateModel import StateModel
from djangocensus.rest_api.serializers import StateSerializer


# Detail viewset goes here.
class StateDetailViewSet(RetrieveAPIView):
    serializer_class = StateSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = StateModel