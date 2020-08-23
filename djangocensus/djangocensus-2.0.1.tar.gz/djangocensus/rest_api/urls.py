from django.conf.urls import re_path, include
from djangocensus.rest_api import viewsets


# Your urlpatterns goes here.
urlpatterns = [
    # urlpatterns for city.
    re_path(r'^city/all/$', viewsets.CityListViewSet.as_view(), name='city_list'),
    re_path(r'^city/create/$', viewsets.CityCreateViewSet.as_view(), name='city_create'),
    re_path(r'^city/(?P<slug>[\w-]+)/$', viewsets.CityDetailViewSet.as_view(), name='city_detail'),
    re_path(r'^city/(?P<slug>[\w-]+)/update/$', viewsets.CityRetrieveUpdateViewSet.as_view(), name='city_update'),
    re_path(r'^city/(?P<slug>[\w-]+)/destroy/$', viewsets.CityDestroyViewSet.as_view(), name='city_destroy'),
    # urlpatterns for continent.
    re_path(r'^continent/all/$', viewsets.ContinentListViewSet.as_view(), name='continent_list'),
    re_path(r'^continent/create/$', viewsets.ContinentCreateViewSet.as_view(), name='continent_create'),
    re_path(r'^continent/(?P<slug>[\w-]+)/$', viewsets.ContinentDetailViewSet.as_view(), name='continent_detail'),
    re_path(r'^continent/(?P<slug>[\w-]+)/update/$', viewsets.ContinentRetrieveUpdateViewSet.as_view(), name='continent_update'),
    re_path(r'^continent/(?P<slug>[\w-]+)/destroy/$', viewsets.ContinentDestroyViewSet.as_view(), name='continent_destroy'),
    # urlpatterns for country.
    re_path(r'^country/all/$', viewsets.CountryListViewSet.as_view(), name='country_list'),
    re_path(r'^country/create/$', viewsets.CountryCreateViewSet.as_view(), name='country_create'),
    re_path(r'^country/(?P<slug>[\w-]+)/$', viewsets.CountryDetailViewSet.as_view(), name='country_detail'),
    re_path(r'^country/(?P<slug>[\w-]+)/update/$', viewsets.CountryRetrieveUpdateViewSet.as_view(), name='country_update'),
    re_path(r'^country/(?P<slug>[\w-]+)/destroy/$', viewsets.CountryDestroyViewSet.as_view(), name='country_destroy'),
    # urlpatterns for state.
    re_path(r'^state/all/$', viewsets.StateListViewSet.as_view(), name='state_list'),
    re_path(r'^state/create/$', viewsets.StateCreateViewSet.as_view(), name='state_create'),
    re_path(r'^state/(?P<slug>[\w-]+)/$', viewsets.StateDetailViewSet.as_view(), name='state_detail'),
    re_path(r'^state/(?P<slug>[\w-]+)/update/$', viewsets.StateRetrieveUpdateViewSet.as_view(), name='state_update'),
    re_path(r'^state/(?P<slug>[\w-]+)/destroy/$', viewsets.StateDestroyViewSet.as_view(), name='state_destroy'),
    # urlpatterns for district.
    re_path(r'^district/all/$', viewsets.DistrictListViewSet.as_view(), name='state_list'),
    re_path(r'^district/create/$', viewsets.DistrictCreateViewSet.as_view(), name='state_create'),
    re_path(r'^district/(?P<slug>[\w-]+)/$', viewsets.DistrictDetailViewSet.as_view(), name='state_detail'),
    re_path(r'^district/(?P<slug>[\w-]+)/update/$', viewsets.DistrictRetrieveUpdateViewSet.as_view(), name='state_update'),
    re_path(r'^district/(?P<slug>[\w-]+)/destroy/$', viewsets.DistrictDestroyViewSet.as_view(), name='state_destroy'),
    # urlpatterns for village.
    re_path(r'^village/all/$', viewsets.VillageListViewSet.as_view(), name='village_list'),
    re_path(r'^village/create/$', viewsets.VillageCreateViewSet.as_view(), name='village_create'),
    re_path(r'^village/(?P<slug>[\w-]+)/$', viewsets.VillageDetailViewSet.as_view(), name='village_detail'),
    re_path(r'^village/(?P<slug>[\w-]+)/update/$', viewsets.VillageRetrieveUpdateViewSet.as_view(), name='village_update'),
    re_path(r'^village/(?P<slug>[\w-]+)/destroy/$', viewsets.VillageDestroyViewSet.as_view(), name='village_destroy'),
    # urlpatterns for religion.
    re_path(r'^religion/all/$', viewsets.ReligionListViewSet.as_view(), name='religion_list'),
    re_path(r'^religion/create/$', viewsets.ReligionCreateViewSet.as_view(), name='religion_create'),
    re_path(r'^religion/(?P<slug>[\w-]+)/$', viewsets.ReligionDetailViewSet.as_view(), name='religion_detail'),
    re_path(r'^religion/(?P<slug>[\w-]+)/update/$', viewsets.ReligionRetrieveUpdateViewSet.as_view(), name='religion_update'),
    re_path(r'^religion/(?P<slug>[\w-]+)/destroy/$', viewsets.ReligionDestroyViewSet.as_view(), name='religion_destroy'),
    # urlpatterns for litracy.
    re_path(r'^litracy/all/$', viewsets.LitracyListViewSet.as_view(), name='litracy_list'),
    re_path(r'^litracy/create/$', viewsets.LitracyCreateViewSet.as_view(), name='litracy_create'),
    re_path(r'^litracy/(?P<slug>[\w-]+)/$', viewsets.LitracyDetailViewSet.as_view(), name='litracy_detail'),
    re_path(r'^litracy/(?P<slug>[\w-]+)/update/$', viewsets.LitracyRetrieveUpdateViewSet.as_view(), name='litracy_update'),
    re_path(r'^litracy/(?P<slug>[\w-]+)/destroy/$', viewsets.LitracyDestroyViewSet.as_view(), name='litracy_destroy'),
    # urlpatterns for population.
    re_path(r'^population/all/$', viewsets.PopulationListViewSet.as_view(), name='population_list'),
    re_path(r'^population/create/$', viewsets.PopulationCreateViewSet.as_view(), name='population_create'),
    re_path(r'^population/(?P<slug>[\w-]+)/$', viewsets.PopulationDetailViewSet.as_view(), name='population_detail'),
    re_path(r'^population/(?P<slug>[\w-]+)/update/$', viewsets.PopulationRetrieveUpdateViewSet.as_view(), name='population_update'),
    re_path(r'^population/(?P<slug>[\w-]+)/destroy/$', viewsets.PopulationDestroyViewSet.as_view(), name='population_destroy'),
    # urlpatterns for religiouspopulation.
    re_path(r'^religiouspopulation/all/$', viewsets.ReligiousPopulationListViewSet.as_view(), name='religiouspopulation_list'),
    re_path(r'^religiouspopulation/create/$', viewsets.ReligiousPopulationCreateViewSet.as_view(), name='religiouspopulation_create'),
    re_path(r'^religiouspopulation/(?P<slug>[\w-]+)/$', viewsets.ReligiousPopulationDetailViewSet.as_view(), name='religiouspopulation_detail'),
    re_path(r'^religiouspopulation/(?P<slug>[\w-]+)/update/$', viewsets.ReligiousPopulationRetrieveUpdateViewSet.as_view(), name='religiouspopulation_update'),
    re_path(r'^religiouspopulation/(?P<slug>[\w-]+)/destroy/$', viewsets.ReligiousPopulationDestroyViewSet.as_view(), name='religiouspopulation_destroy'),
]