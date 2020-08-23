from rest_framework.generics import RetrieveAPIView
from djangocensus.models.VillageModel import VillageModel
from djangocensus.rest_api.serializers import VillageSerializer


# Detail viewset goes here.
class VillageDetailViewSet(RetrieveAPIView):
    serializer_class = VillageSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = VillageModel