from rest_framework.generics import ListAPIView
from djangocensus.models.VillageModel import VillageModel
from djangocensus.rest_api.serializers import VillageSerializer


# List viewset goes here.
class VillageListViewSet(ListAPIView):
    serializer_class = VillageSerializer
    queryset = VillageModel.objects.all()