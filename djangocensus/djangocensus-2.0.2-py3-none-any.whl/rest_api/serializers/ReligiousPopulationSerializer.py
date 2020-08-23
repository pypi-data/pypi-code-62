from rest_framework.serializers import ModelSerializer
from djangocensus.models import ReligiousPopulationModel


# Your serializers goes here.
class ReligiousPopulationSerializer(ModelSerializer):
    class Meta:
        model = ReligiousPopulationModel
        fields = "__all__"
