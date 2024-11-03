from django_filters import FilterSet, BooleanFilter, DateFilter, CharFilter
# , ChoiceFilter
from .models import Risk, Prj

class RiskFilter(FilterSet):
    # status = ChoiceFilter(choices=Risk.status)
    escalated = BooleanFilter(label='Escalated')
    # date_last_updated = DateFilter(lookup_expr='range')
    start_date = DateFilter(field_name='date_last_updated', lookup_expr='gte')
    end_date = DateFilter(field_name='date_last_updated', lookup_expr='lte')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    owner = CharFilter(field_name='owner', lookup_expr='icontains')

    class Meta:
        model = Risk
        fields = ['name', 'category', 'owner', 'status', 'escalated', 'start_date', 'end_date']

class ProjectFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Prj
        fields = ['name', 'status']