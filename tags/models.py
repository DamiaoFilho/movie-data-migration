from django.db import models
from movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Tag(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Filme")  
    user_id = models.IntegerField(verbose_name="ID do usuário")  
    tag = models.CharField(max_length=255)  
    timestamp = models.DateTimeField(verbose_name="Data de criação")  

    def __str__(self):
        return f'User {self.user_id} - Movie {self.movie}: {self.tag}'
    

class GenomeScore(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Filme")  
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Tag")  
    relevance = models.FloatField(
        verbose_name="Relevância",
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ]
    )  
    
    def __str__(self) -> str:
        return f'{self.movie} - {self.tag}: {self.relevance}'


class GenomeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Tag")  
    tag_details = models.CharField(max_length=255, verbose_name="Detalhes")  

    def __str__(self):
        return f'{self.tag}: {self.tag_details}'
