from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    titulo = models.CharField('Titulo', max_length=100, blank=False, null=False)
    descricao = models.TextField('Descrição', blank=True, null=True)
    cnpj = models.CharField('CNPJ', max_length=20, blank=False, null=False)
    data_agendamento = models.DateTimeField('Data de agendamento', blank=False, null=False)
    duracao = models.IntegerField('Duração tarefa', blank=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
