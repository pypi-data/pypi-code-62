from rest_framework.serializers import ModelSerializer
from djangocensus.models import StateModel


# Your serializers goes here.
class StateSerializer(ModelSerializer):
    class Meta:
        model = StateModel
        fields = "__all__"
