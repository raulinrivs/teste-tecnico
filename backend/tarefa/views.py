# Django imports
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from config import settings
# Models imports
from tarefa.models import Tarefa
from django.contrib.auth.models import User
# REST Framework imports
from rest_framework import viewsets, generics, permissions, \
    authentication, status, views
from rest_framework.response import Response
from tarefa.serializers import CSRFTokenSerializer, LoginSerializer, TarefaSerializer, UserSerializer
# Tasks imports
from tarefa.tasks import add_tarefa
from config.celery import app


class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    http_method_names = ['get', 'patch', 'delete', 'post']
    serializer_class = TarefaSerializer
    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        if serializer.is_valid():
            task = add_tarefa.apply_async(countdown=30, kwargs={
                'titulo': serializer.validated_data.get('titulo'),
                'descricao': serializer.validated_data.get('descricao'),
                'cnpj': serializer.validated_data.get('cnpj'),
                'data_agendamento': serializer.validated_data.get('data_agendamento'),
                'duracao': serializer.validated_data.get('duracao'),
                'usuario': serializer.validated_data.get('usuario_id')
            })
            # task = app.send_task('tarefa.tasks.add_tarefa', kwargs={
            #     'titulo': serializer.validated_data.get('titulo'),
            #     'descricao': serializer.validated_data.get('descricao'),
            #     'cnpj': serializer.validated_data.get('cnpj'),
            #     'data_agendamento': serializer.validated_data.get('data_agendamento'),
            #     'duracao': serializer.validated_data.get('duracao'),
            #     'usuario': serializer.validated_data.get('usuario_id')
            # })
            print(task.id)
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete', 'post']
    serializer_class = UserSerializer
    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]


class LoginAPIViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if request.user.is_authenticated:
            return Response(
                {'detail': 'Voce já está logado'},
                status=status.HTTP_400_BAD_REQUEST)

        if username is None or password is None:
            return Response(
                {'detail': 'Favor inserir senha e matricula'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'detail': 'Credenciais inválidas'},
                            status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class LogoutAPIViewSet(views.APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Você não está logado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return Response({'detail': 'Usuário deslogado com sucesso.'},
                        status=status.HTTP_200_OK)


class SessionValidatorViewSet(views.APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'isLoggedIn': False})

        return Response({'isLoggedIn': True, 'username': request.user.username})


class WhoAmIViewSet(views.APIView):
    serializer_class = UserSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'isLoggedIn': False, 'username': None},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.serializer_class(User.objects.get(id=request.user.id))
        return Response(user.data, status=status.HTTP_200_OK)
    

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenAPIViewSet(generics.GenericAPIView):
    serializer_class = CSRFTokenSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        response = Response(data={'X-CSRFToken': get_token(request)},
                            status=status.HTTP_200_OK)
        return response