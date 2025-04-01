from django.db import models
from .factory_model import FactoryModel

def aula_upload_path(instance, filename):
    return f'aulas/conteudo/{instance.id}/{filename}'


class Aula(FactoryModel):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    turma = models.ForeignKey('Turma', related_name='aulas', on_delete=models.CASCADE, null=True, blank=True)
    conteudo = models.FileField(upload_to = aula_upload_path)
    atividade = models.ForeignKey('Atividade', on_delete=models.DO_NOTHING, related_name='aulas', null=True, blank=True)
    data_aula = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'aula'
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['data_aula']
    

