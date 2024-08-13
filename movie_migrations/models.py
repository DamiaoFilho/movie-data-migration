from django.db import models

# Create your models here.

class MovieMigration(models.Model):
    
    class Status(models.TextChoices):
        PROCESSING = 'processing', 'Processando'
        COMPLETED = 'completed', 'Concluído'
        ERROR = 'error', 'Erro'
    
    
    total_time = models.FloatField(verbose_name="Tempo total", default=0)
    data_quantity = models.IntegerField(verbose_name="Quantidade de dados", default=0)
    registry_erros_number = models.IntegerField(verbose_name="Quantidade de erros de registro", default=0)
    file = models.FileField(upload_to='uploads/', verbose_name="Arquivo")
    model = models.CharField(max_length=255, verbose_name="Modelo", null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROCESSING,
        verbose_name="Status"
    )
    
    def __str__(self) -> str:
        return f'{self.file}: {self.total_time} - {self.model}'
    
    class Meta:
        verbose_name = "Migração de Dados"
        verbose_name_plural = "Migrações de Dados"