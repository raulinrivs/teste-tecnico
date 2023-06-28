from django.urls import include, path
from rest_framework import routers
# from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from tarefa.views import CSRFTokenAPIViewSet, LoginAPIViewSet, LogoutAPIViewSet, SessionValidatorViewSet, TarefaViewSet, UserViewSet, WhoAmIViewSet

router = routers.DefaultRouter()

router.register(r'tarefa', TarefaViewSet)
router.register(r'user', UserViewSet)

SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title='API Tarefas',
        default_version='v1',
        description='API Teste Técnico Fontes feito por Mateus Raulino',
        contact=openapi.Contact(name='Mateus Raulino', email='mr.mraulino@gmail.com', url='https://www.linkedin.com/in/mateusraulino97/'),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    # path('tarefa/', TarefaViewSet.as_view(), name='tarefa'),
    path('swagger<str:format>', SCHEMA_VIEW.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', SCHEMA_VIEW.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SCHEMA_VIEW.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('accounts/login/', LoginAPIViewSet.as_view(), name='api-login'),
    path('accounts/logout/', LogoutAPIViewSet.as_view(), name='api-logout'),
    path('accounts/session/', SessionValidatorViewSet.as_view(), name='api-session'),
    path('accounts/whoami/', WhoAmIViewSet.as_view(), name='api-whoami'),
    path('csrf/', CSRFTokenAPIViewSet.as_view(), name='api-csrf'),
]