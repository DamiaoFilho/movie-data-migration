from django.db import models
from movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Tag(models.Model):
    movieId = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Filme")  
    userId = models.IntegerField(verbose_name="ID do usuário")  
    tag = models.CharField(max_length=255)  
    timestamp = models.DateTimeField(verbose_name="Data de criação")  

    def __str__(self):
        return f'User {self.userId} - Movie {self.movieId}: {self.tag}'
    

class GenomeScore(models.Model):
    movieId = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Filme")  
    tagId = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Tag")  
    relevance = models.FloatField(
        verbose_name="Relevância",
        validators=[
            MinValueValidator(0.5),
            MaxValueValidator(5.0)
        ]
    )  


class GenomeTag(models.Model):
    tagId = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Tag")  
    tag = models.CharField(max_length=255, verbose_name="Detalhes")  

    def __str__(self):
        return self.tag
