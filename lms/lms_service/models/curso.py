from django.db import models
from .factory_model import FactoryModel

class Curso(FactoryModel):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'curso'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'