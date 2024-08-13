from django_filters import FilterSet
import django_filters
from .models import MovieMigration
from django.db import models
from movies.models import Movie
from django.db.models import Avg, Count
import re

class MigrationFilterSet(FilterSet):

    class ModelChoices(models.TextChoices):
        MOVIE = 'filmes', 'Filmes'
        LINKS = 'links', 'Links'
        TAGS = 'tags', 'Tags'
        RATINGS = 'avaliacoes', 'Avaliações'
        GENOME_TAGS = 'Tags do Genoma', 'Genome Tags'
        GENOME_SCORES = 'Pontuações do Genoma', 'Genome Scores'

    model = django_filters.ChoiceFilter(
        field_name='model',
        lookup_expr='icontains',
        label='Modelo',
        choices=ModelChoices.choices
    )
    total_time = django_filters.NumericRangeFilter(label='Intervalo de tempo')
    data_quantity = django_filters.NumericRangeFilter(label='Quantidade de dados')
    registry_erros_number = django_filters.NumericRangeFilter(label='Quantidade de erros de registro')

    class Meta:
        model = MovieMigration
        fields = ['total_time', 'data_quantity', 'registry_erros_number', 'model']


class MovieFilterSet(django_filters.FilterSet):
    genres = django_filters.ChoiceFilter(field_name='genres', lookup_expr='icontains', label='Gênero')
    release_year = django_filters.NumericRangeFilter(field_name='release_year', label='Ano de lançamento')
    average_rating = django_filters.NumberFilter(field_name='average_rating', label='Avaliação mínima')
    rating_count = django_filters.NumberFilter(field_name='rating_count', lookup_expr='gte', label='Quantidade mínima de avaliações')
    user_id = django_filters.NumberFilter(method='filter_by_user_id', label='ID do usuário')

    def filter_by_user_id(self, queryset, name, value):
        return queryset.filter(tag__user_id=value)

    class Meta:
        model = Movie
        queryset = Movie.objects.all()
        queryset = queryset.annotate(
            average_rating=Avg('genomescore__relevance'),
            rating_count=Count('genomescore')
        ).select_related('tag')

        fields = ['genres', 'release_year', 'average_rating', 'rating_count', 'user_id']