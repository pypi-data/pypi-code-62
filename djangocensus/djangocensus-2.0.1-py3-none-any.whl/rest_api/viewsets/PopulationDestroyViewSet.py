from rest_framework.generics import DestroyAPIView
from djangocensus.models.PopulationModel import PopulationModel
from djangocensus.rest_api.serializers import PopulationSerializer


# Create viewset goes here.
class PopulationDestroyViewSet(DestroyAPIView):
    serializer_class = PopulationSerializer
    queryset = PopulationModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
