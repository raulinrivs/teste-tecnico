from __future__ import absolute_import, unicode_literals
from tarefa.models import Tarefa
from config.celery import app
from django.core.mail import send_mail

@app.task(serializer='json')
def add_tarefa(titulo, descricao, cnpj, data_agendamento, duracao, usuario):
    return Tarefa.objects.create(
        titulo = titulo,
        descricao = descricao,
        cnpj = cnpj,
        data_agendamento = data_agendamento,
        duracao = duracao,
        usuario_id = usuario
    )

@app.task
def emails():
    send_mail(
    "Subject here",
    "Here is the message.",
    "from@example.com",
    ["to@example.com"],
    fail_silently=False,
)