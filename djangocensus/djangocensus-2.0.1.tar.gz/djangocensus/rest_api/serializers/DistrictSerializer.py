from rest_framework.serializers import ModelSerializer
from djangocensus.models import DistrictModel


# Your serializers goes here.
class DistrictSerializer(ModelSerializer):
    class Meta:
        model = DistrictModel
        fields = "__all__"
