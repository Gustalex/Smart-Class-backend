from django.db import models
from .factory_model import FactoryModel

def aula_upload_path(instance, filename):
    return f'aulas/conteudo/{instance.id}/{filename}'


class Aula(FactoryModel):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    conteudo = models.FileField(upload_to = aula_upload_path)
    atividade = models.ForeignKey('Atividade', related_name='aulas')

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'aula'
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['titulo']
    

