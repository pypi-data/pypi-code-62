from rest_framework.generics import DestroyAPIView
from djangocensus.models.VillageModel import VillageModel
from djangocensus.rest_api.serializers import VillageSerializer


# Create viewset goes here.
class VillageDestroyViewSet(DestroyAPIView):
    serializer_class = VillageSerializer
    queryset = VillageModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
