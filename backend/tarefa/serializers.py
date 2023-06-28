from rest_framework import serializers
from tarefa.models import Tarefa
from django.contrib.auth.models import User

class TarefaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    usuario_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Tarefa
        fields = ('id', 'titulo', 'descricao', 'cnpj', 'data_agendamento', 'duracao', 'usuario_id')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('username', 'password')


class CSRFTokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ('token')