from django.db import models

# Create your models here.

class MovieMigration(models.Model):
    total_time = models.FloatField(verbose_name="Tempo total")
    data_quantity = models.IntegerField(verbose_name="Quantidade de dados")
    registry_erros_number = models.IntegerField(verbose_name="Quantidade de erros de registro", default=0)

