from django.shortcuts import render
from rest_framework import viewsets,status
from .serializers import UsuarioSerializer,TipoSerializer,ProductoSerializer
from .models import Usuario,Tipo_Producto,Producto
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS,exceptions,AllowAny
from rest_framework.authentication import TokenAuthentication
# Create your views here.


class UsuarioList(APIView):
    def get(self, request, format=None):
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer = UsuarioSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            cuenta = serializer.save()
            data['username'] = cuenta.username
            token = Token.objects.get(user=cuenta).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

class UsuarioEdit(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,id_usuario):
        try:
            return Usuario.objects.get(id_usuario=id_usuario)
        except Usuario.DoesNotExist:
            raise Http404

    def get(self,request,id_usuario=None):
        usuario = self.get_object(id_usuario)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    def delete(self, request, id_usuario=None):
        usuario = self.get_object(id_usuario)
        usuario.delete()
        return Response('eliminado correctamente')
        
    def put(self,request,id_usuario,format=None):
        user = self.get_object(id_usuario)
        serializer = UsuarioSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS