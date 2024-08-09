from django.db import models

# Create your models here.
from ..movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    movieId = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Filme")  
    userId = models.IntegerField(verbose_name="ID do Usuário")  
    rating = models.FloatField(
        verbose_name="Avaliação",
        validators=[
            MinValueValidator(0.5),
            MaxValueValidator(5.0)
        ]
    )  
    timestamp = models.DateTimeField()  

    def __str__(self):
        return f'User {self.userId} - Movie {self.movieId}: {self.rating}'