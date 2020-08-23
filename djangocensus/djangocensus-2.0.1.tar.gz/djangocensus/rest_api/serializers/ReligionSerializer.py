from rest_framework.serializers import ModelSerializer
from djangocensus.models import ReligionModel


# Your serializers goes here.
class ReligionSerializer(ModelSerializer):
    class Meta:
        model = ReligionModel
        fields = "__all__"