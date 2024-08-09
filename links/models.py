from django.db import models
from ..movies.models import Movie

# Create your models here.
class Link(models.Model):
    movieId = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Filme")  
    imdbId = models.CharField(max_length=20)  
    tmdbId = models.CharField(max_length=20)  

    def __str__(self):
        return f'Links for Movie {self.movieId}'