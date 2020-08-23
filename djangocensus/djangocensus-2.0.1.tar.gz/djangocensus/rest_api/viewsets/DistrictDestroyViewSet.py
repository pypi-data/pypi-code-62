from rest_framework.generics import DestroyAPIView
from djangocensus.models.DistrictModel import DistrictModel
from djangocensus.rest_api.serializers import DistrictSerializer


# Create viewset goes here.
class DistrictDestroyViewSet(DestroyAPIView):
    serializer_class = DistrictSerializer
    queryset = DistrictModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
