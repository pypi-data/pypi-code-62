from rest_framework.generics import ListAPIView
from djangocensus.models.ReligionModel import ReligionModel
from djangocensus.rest_api.serializers import ReligionSerializer


# List viewset goes here.
class ReligionListViewSet(ListAPIView):
    serializer_class = ReligionSerializer
    queryset = ReligionModel.objects.all()