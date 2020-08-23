from rest_framework.serializers import ModelSerializer
from djangocensus.models import ContinentModel


# Your serializers goes here.
class ContinentSerializer(ModelSerializer):
    class Meta:
        model = ContinentModel
        fields = "__all__"
        depth = 1
