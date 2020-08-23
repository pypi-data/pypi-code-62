from rest_framework.serializers import ModelSerializer
from djangocensus.models import CityModel


# Your serializers goes here.
class CitySerializer(ModelSerializer):
    class Meta:
        model = CityModel
        fields = "__all__"
