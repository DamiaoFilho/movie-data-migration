from django.db import models

class Movie(models.Model):
    movieId = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)  
    genres = models.CharField(max_length=255)  

    def __str__(self):
        return self.title
