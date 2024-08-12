from django.db import models

# Create your models here.

class MovieMigration(models.Model):
    total_time = models.FloatField(verbose_name="Tempo total")
    data_quantity = models.IntegerField(verbose_name="Quantidade de dados")
    registry_erros_number = models.IntegerField(verbose_name="Quantidade de erros de registro", default=0)
    file = models.FileField(upload_to='uploads/', verbose_name="Arquivo")
    model = models.CharField(max_length=255, verbose_name="Modelo")
    
    
    def __str__(self) -> str:
        return f'{self.file} - {self.total_time} - {self.data_quantity} - {self.registry_erros_number}'