from rest_framework.generics import RetrieveAPIView
from djangocensus.models.PopulationModel import PopulationModel
from djangocensus.rest_api.serializers import PopulationSerializer


# Detail viewset goes here.
class PopulationDetailViewSet(RetrieveAPIView):
    serializer_class = PopulationSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = PopulationModel