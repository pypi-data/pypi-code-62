from rest_framework.generics import ListAPIView
from djangocensus.models.StateModel import StateModel
from djangocensus.rest_api.serializers import StateSerializer


# List viewset goes here.
class StateListViewSet(ListAPIView):
    serializer_class = StateSerializer
    queryset = StateModel.objects.all()