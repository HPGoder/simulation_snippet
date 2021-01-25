import django_filters
from django_filters import CharFilter, ChoiceFilter
from projects.models import project, AcceptanceCriteria, weld_configuration

class ECAfilter(django_filters.FilterSet):

    ECA_LIST = AcceptanceCriteria.objects.all()
    query_LIST = [eca.name for eca in ECA_LIST]
    CHOICES_LIST = tuple([tuple([str(item.name), item.name]) for item in ECA_LIST])
    name = ChoiceFilter(field_name = "name", choices = CHOICES_LIST)

    class Meta :

        model = AcceptanceCriteria
        fields = ('name',)


class WeldConfigfilter(django_filters.FilterSet):

    WELD_LIST = weld_configuration.objects.all()
    VESSEL_CHOICES_LIST = tuple([tuple([str(item.vessel), item.vessel]) for item in WELD_LIST])
    STATION_CHOICES_LIST = tuple([tuple([str(item.station), item.station]) for item in WELD_LIST])
    vessel = ChoiceFilter(field_name = "vessel", choices = VESSEL_CHOICES_LIST)
    station= ChoiceFilter(field_name = "station", choices = STATION_CHOICES_LIST)
    class Meta:
        model = weld_configuration
        fields = ('vessel', 'station')