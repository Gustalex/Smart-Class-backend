from django.db import models 

def conteudo_para_avaliacao_path(instance, filename):
    return f'conteudo_avaliacao/{instance.aluno}/{filename}'

class AvaliacaoAtividade(models.Model):
    aluno = models.IntegerField()
    atividade = models.IntegerField()
    conteudo_para_avaliacao = models.FileField(upload_to=conteudo_para_avaliacao_path)
    nota = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Avaliação de Atividade: {self.aluno} - {self.atividade} - {self.nota}"
    
    class Meta:
        db_table = 'avaliacao_atividade'
        verbose_name = 'Avaliação de Atividade'
        verbose_name_plural = 'Avaliações de Atividades'
        ordering = ['atividade', 'aluno']