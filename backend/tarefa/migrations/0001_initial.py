# Generated by Django 4.2.2 on 2023-06-21 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('cnpj', models.CharField(max_length=20, verbose_name='CNPJ')),
                ('data_agendamento', models.DateTimeField(verbose_name='Data de agendamento')),
                ('duracao', models.IntegerField(verbose_name='Duração tarefa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
