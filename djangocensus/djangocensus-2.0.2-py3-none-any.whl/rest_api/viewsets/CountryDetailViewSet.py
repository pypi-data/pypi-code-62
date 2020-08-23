from rest_framework.generics import RetrieveAPIView
from djangocensus.models.CountryModel import CountryModel
from djangocensus.rest_api.serializers import CountrySerializer


# Detail viewset goes here.
class CountryDetailViewSet(RetrieveAPIView):
    serializer_class = CountrySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = CountryModel