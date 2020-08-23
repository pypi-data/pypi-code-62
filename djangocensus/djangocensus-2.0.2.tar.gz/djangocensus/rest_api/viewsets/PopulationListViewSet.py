from rest_framework.generics import ListAPIView
from djangocensus.models.PopulationModel import PopulationModel
from djangocensus.rest_api.serializers import PopulationSerializer


# List viewset goes here.
class PopulationListViewSet(ListAPIView):
    serializer_class = PopulationSerializer
    queryset = PopulationModel.objects.all()