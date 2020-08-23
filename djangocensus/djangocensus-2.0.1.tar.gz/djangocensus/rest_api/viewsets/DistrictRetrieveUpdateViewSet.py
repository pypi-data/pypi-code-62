from rest_framework.generics import RetrieveUpdateAPIView
from djangocensus.models.DistrictModel import DistrictModel
from djangocensus.rest_api.serializers import DistrictSerializer


# Create viewset goes here.
class DistrictRetrieveUpdateViewSet(RetrieveUpdateAPIView):
    serializer_class = DistrictSerializer
    queryset = DistrictModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"