from rest_framework.generics import RetrieveAPIView
from djangocensus.models.ReligionModel import ReligionModel
from djangocensus.rest_api.serializers import ReligionSerializer


# Detail viewset goes here.
class ReligionDetailViewSet(RetrieveAPIView):
    serializer_class = ReligionSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = ReligionModel