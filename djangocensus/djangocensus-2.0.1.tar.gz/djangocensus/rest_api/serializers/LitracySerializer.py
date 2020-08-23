from rest_framework.serializers import ModelSerializer
from djangocensus.models import LitracyModel


# Your serializers goes here.
class LitracySerializer(ModelSerializer):
    class Meta:
        model = LitracyModel
        fields = "__all__"
