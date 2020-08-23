from rest_framework.generics import RetrieveAPIView
from djangocensus.models.ReligiousPopulationModel import ReligiousPopulationModel
from djangocensus.rest_api.serializers import ReligiousPopulationSerializer


# Detail viewset goes here.
class ReligiousPopulationDetailViewSet(RetrieveAPIView):
    serializer_class = ReligiousPopulationSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = ReligiousPopulationModel