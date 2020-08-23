from rest_framework.serializers import ModelSerializer
from djangocensus.models import CountryModel


# Your serializers goes here.
class CountrySerializer(ModelSerializer):
    class Meta:
        model = CountryModel
        fields = "__all__"
