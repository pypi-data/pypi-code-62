from rest_framework.generics import CreateAPIView
from djangocensus.models.CountryModel import CountryModel
from djangocensus.rest_api.serializers import CountrySerializer


# Create viewset goes here.
class CountryCreateViewSet(CreateAPIView):
    serializer_class = CountrySerializer
    queryset = CountryModel

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)