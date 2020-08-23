from rest_framework.generics import DestroyAPIView
from djangocensus.models.ContinentModel import ContinentModel
from djangocensus.rest_api.serializers import ContinentSerializer


# Create viewset goes here.
class ContinentDestroyViewSet(DestroyAPIView):
    serializer_class = ContinentSerializer
    queryset = ContinentModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"