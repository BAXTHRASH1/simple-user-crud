from django.contrib import admin
from django.urls import path
from .views import UsuarioList,UsuarioEdit
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('usuario/',UsuarioList.as_view()),
    path('usuariodetail/<int:id_usuario>/',UsuarioEdit.as_view()),
    path('login/',obtain_auth_token,name='login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)