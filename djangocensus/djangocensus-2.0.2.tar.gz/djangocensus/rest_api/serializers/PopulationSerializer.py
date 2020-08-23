from rest_framework.serializers import ModelSerializer
from djangocensus.models import PopulationModel


# Your serializers goes here.
class PopulationSerializer(ModelSerializer):
    class Meta:
        model = PopulationModel
        fields = "__all__"
