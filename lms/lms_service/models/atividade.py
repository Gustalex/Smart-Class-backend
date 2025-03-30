from django.db import models
from .factory_model import FactoryModel

def atividade_upload_path(instance, filename):
    return f'atividades/conteudo/{instance.id}/{filename}'


class Atividade(FactoryModel):
    titulo = models.CharField(max_length = 255)
    descricao = models.TextField()
    conteudo = models.FileField(upload_to = atividade_upload_path)
    aula = models.ForeignKey('Aula', related_name='atividades', on_delete=models.CASCADE)
    data_entrega = models.DateTimeField()

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'atividade'
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['data_entrega']

