from rest_framework.generics import RetrieveUpdateAPIView
from djangocensus.models.ReligiousPopulationModel import ReligiousPopulationModel
from djangocensus.rest_api.serializers import ReligiousPopulationSerializer


# Create viewset goes here.
class ReligiousPopulationRetrieveUpdateViewSet(RetrieveUpdateAPIView):
    serializer_class = ReligiousPopulationSerializer
    queryset = ReligiousPopulationModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"