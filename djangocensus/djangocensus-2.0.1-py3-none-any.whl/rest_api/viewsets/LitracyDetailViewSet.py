from rest_framework.generics import RetrieveAPIView
from djangocensus.models.LitracyModel import LitracyModel
from djangocensus.rest_api.serializers import LitracySerializer


# Detail viewset goes here.
class LitracyDetailViewSet(RetrieveAPIView):
    serializer_class = LitracySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = LitracyModel