from rest_framework.generics import ListAPIView
from djangocensus.models.ContinentModel import ContinentModel
from djangocensus.rest_api.serializers import ContinentSerializer


# List viewset goes here.
class ContinentListViewSet(ListAPIView):
    serializer_class = ContinentSerializer
    queryset = ContinentModel.objects.all()