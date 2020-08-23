from rest_framework.generics import DestroyAPIView
from djangocensus.models.LitracyModel import LitracyModel
from djangocensus.rest_api.serializers import LitracySerializer


# Create viewset goes here.
class LitracyDestroyViewSet(DestroyAPIView):
    serializer_class = LitracySerializer
    queryset = LitracyModel
    lookup_field = "slug"
    lookup_url_kwarg = "slug"