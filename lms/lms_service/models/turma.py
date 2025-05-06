from django.db import models
from .factory_model import FactoryModel

class Turma(FactoryModel):
    nome = models.CharField(max_length=255, unique=True)
    curso = models.ForeignKey('Curso', related_name='turmas', on_delete=models.CASCADE)
    professor = models.IntegerField()
    alunos = models.JSONField()

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'turma'
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['nome']