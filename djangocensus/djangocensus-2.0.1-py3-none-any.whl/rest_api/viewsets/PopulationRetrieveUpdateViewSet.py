from rest_framework.generics import RetrieveUpdateAPIView
from djangocensus.models.PopulationModel import PopulationModel
from djangocensus.rest_api.serializers import PopulationSerializer


# Create viewset goes here.
class PopulationRetrieveUpdateViewSet(RetrieveUpdateAPIView):
    serializer_class = PopulationSerializer
    queryset = PopulationModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"