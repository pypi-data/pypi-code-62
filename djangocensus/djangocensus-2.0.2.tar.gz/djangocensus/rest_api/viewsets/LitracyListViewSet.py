from rest_framework.generics import ListAPIView
from djangocensus.models.LitracyModel import LitracyModel
from djangocensus.rest_api.serializers import LitracySerializer


# List viewset goes here.
class LitracyListViewSet(ListAPIView):
    serializer_class = LitracySerializer
    queryset = LitracyModel.objects.all()