from django.contrib import admin
from djangocensus.models import ContinentModel
from djangocensus.models import CountryModel
from djangocensus.models import StateModel
from djangocensus.models import DistrictModel
from djangocensus.models import CityModel
from djangocensus.models import VillageModel
from djangocensus.models import ReligiousPopulationModel
from djangocensus.models import ReligionModel
from djangocensus.models import PopulationModel
from djangocensus.models import LitracyModel
from djangocensus.modeladmins import ContinentModelAdmin
from djangocensus.modeladmins import CountryModelAdmin
from djangocensus.modeladmins import StateModelAdmin
from djangocensus.modeladmins import DistrictModelAdmin
from djangocensus.modeladmins import CityModelAdmin
from djangocensus.modeladmins import VillageModelAdmin
from djangocensus.modeladmins import ReligiousPopulationModelAdmin
from djangocensus.modeladmins import ReligionModelAdmin
from djangocensus.modeladmins import PopulationModelAdmin
from djangocensus.modeladmins import LitracyModelAdmin


# Register your models here.
admin.site.register(ContinentModel, ContinentModelAdmin)
admin.site.register(CountryModel, CountryModelAdmin)
admin.site.register(StateModel, StateModelAdmin)
admin.site.register(DistrictModel, DistrictModelAdmin)
admin.site.register(CityModel, CityModelAdmin)
admin.site.register(VillageModel, VillageModelAdmin)
admin.site.register(ReligiousPopulationModel, ReligiousPopulationModelAdmin)
admin.site.register(ReligionModel, ReligionModelAdmin)
admin.site.register(PopulationModel, PopulationModelAdmin)
admin.site.register(LitracyModel, LitracyModelAdmin)