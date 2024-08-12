from django_filters import FilterSet
from .models import MovieMigration

class YourModelFilter(FilterSet):
    class Meta:
        model = MovieMigration
        fields = {
            'total_time': ['exact', 'lt', 'gt'],
            'data_quantity': ['exact', 'lt', 'gt'],
            'registry_erros_number': ['exact', 'lt', 'gt'],
        }

