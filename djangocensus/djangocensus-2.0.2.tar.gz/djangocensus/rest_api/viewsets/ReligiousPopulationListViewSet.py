from rest_framework.generics import ListAPIView
from djangocensus.models.ReligiousPopulationModel import ReligiousPopulationModel
from djangocensus.rest_api.serializers import ReligiousPopulationSerializer


# List viewset goes here.
class ReligiousPopulationListViewSet(ListAPIView):
    serializer_class = ReligiousPopulationSerializer
    queryset = ReligiousPopulationModel.objects.all()