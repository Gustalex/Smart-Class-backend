from django.db import models


class Recomendacao(models.Model):
    aluno = models.IntegerField()
    atividade = models.IntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recomendacao {self.id} - Aluno {self.aluno} - Atividade {self.atividade}"
    
    class Meta:
        verbose_name = "Recomendação"
        verbose_name_plural = "Recomendações"
        ordering = ["aluno", "atividade"]
    