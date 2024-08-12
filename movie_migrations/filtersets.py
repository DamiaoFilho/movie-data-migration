from django_filters import FilterSet
import django_filters
from .models import MovieMigration

class MigrationFilterSet(FilterSet):
    model = django_filters.CharFilter(lookup_expr='icontains', label='Modelo')
    total_time = django_filters.RangeFilter(label='Tempo total')
    data_quantity = django_filters.RangeFilter(label='Quantidade de dados')
    registry_erros_number = django_filters.RangeFilter(label='Erros de registro')

    class Meta:
        model = MovieMigration
        fields = ['total_time', 'data_quantity', 'registry_erros_number', 'model']


