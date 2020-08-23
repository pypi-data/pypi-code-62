from rest_framework.generics import ListAPIView
from djangocensus.models.CountryModel import CountryModel
from djangocensus.rest_api.serializers import CountrySerializer


# List viewset goes here.
class CountryListViewSet(ListAPIView):
    serializer_class = CountrySerializer
    queryset = CountryModel.objects.all()