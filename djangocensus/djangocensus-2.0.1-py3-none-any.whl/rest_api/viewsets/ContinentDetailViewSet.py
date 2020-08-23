from rest_framework.generics import RetrieveAPIView
from djangocensus.models.ContinentModel import ContinentModel
from djangocensus.rest_api.serializers import ContinentSerializer


# Detail viewset goes here.
class ContinentDetailViewSet(RetrieveAPIView):
    serializer_class = ContinentSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = ContinentModel