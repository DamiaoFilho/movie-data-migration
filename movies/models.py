from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)  
    genres = models.CharField(max_length=255)  
    release_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Filme"
        verbose_name_plural = "Filmes"

