from rest_framework.generics import ListAPIView
from djangocensus.models.DistrictModel import DistrictModel
from djangocensus.rest_api.serializers import DistrictSerializer


# List viewset goes here.
class DistrictListViewSet(ListAPIView):
    serializer_class = DistrictSerializer
    queryset = DistrictModel.objects.all()