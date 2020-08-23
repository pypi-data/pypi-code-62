from rest_framework.serializers import ModelSerializer
from djangocensus.models import VillageModel


# Your serializers goes here.
class VillageSerializer(ModelSerializer):
    class Meta:
        model = VillageModel
        fields = "__all__"
