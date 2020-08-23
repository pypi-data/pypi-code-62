from rest_framework.generics import DestroyAPIView
from djangocensus.models.ReligionModel import ReligionModel
from djangocensus.rest_api.serializers import ReligionSerializer


# Create viewset goes here.
class ReligionDestroyViewSet(DestroyAPIView):
    serializer_class = ReligionSerializer
    queryset = ReligionModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"