from rest_framework.generics import RetrieveAPIView
from djangocensus.models.DistrictModel import DistrictModel
from djangocensus.rest_api.serializers import DistrictSerializer


# Detail viewset goes here.
class DistrictDetailViewSet(RetrieveAPIView):
    serializer_class = DistrictSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = DistrictModel