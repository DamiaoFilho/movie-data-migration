from django.views.generic import FormView
from .forms import MigrationForm
from movies.models import Movie
from ratings.models import Rating
from links.models import Link
from tags.models import Tag, GenomeScore, GenomeTag
from .models import MovieMigration
from django_filters.views import FilterView
from .filtersets import MigrationFilterSet
from .celery import handle_movie_file, handle_movie_depedent_file, handle_link_file, handle_tag_depedent_file


class MigrationView(FormView):
    template_name = "base.html"
    form_class = MigrationForm
    success_url = "/"
    
    def form_valid(self, form):
        data_type = form.cleaned_data['data_type']
        file = form.cleaned_data['file']
        
        migration = MovieMigration.objects.create(file=file)
        if data_type == 'movie':
            migration.model = Movie._meta.verbose_name_plural.title()
            migration.save()
            handle_movie_file.delay(migration.id, ['id', 'title', 'genres'])
        elif data_type == 'ratings':
            migration.model = Rating._meta.verbose_name_plural.title()
            migration.save()
            handle_movie_depedent_file.delay(migration.id, ['user_id', 'movie_id', 'rating', 'timestamp'])
        elif data_type == 'tags':
            migration.model = Tag._meta.verbose_name_plural.title()
            migration.save()
            handle_movie_depedent_file.delay(migration.id, ['user_id', 'movie_id', 'tag', 'timestamp'])
        elif data_type == 'links':
            migration.model = Link._meta.verbose_name_plural.title()
            migration.save()
            handle_link_file.delay(migration.id, ['movie_id', 'imdb_id', 'tmdb_id'])
        elif data_type == 'genome_tags':
            migration.model = GenomeTag._meta.verbose_name_plural
            migration.save()
            handle_tag_depedent_file.delay(migration.id, ['tag_id', 'tag_details'])
        elif data_type == 'genome_scores':
            migration.model = GenomeScore._meta.verbose_name_plural
            migration.save()
            print(migration.model)
            handle_tag_depedent_file.delay(migration.id, ['movie_id', 'tag_id', 'relevance'])
        
        return super().form_valid(form)

class InfoFile(FilterView):
    template_name = "migrations/migration_list.html"
    model = MovieMigration
    paginate_by = 10
    filterset_class = MigrationFilterSet
    context_object_name = 'migrations'
    
    def get_queryset(self):
        return MovieMigration.objects.all()