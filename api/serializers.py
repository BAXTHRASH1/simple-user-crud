from .models import Usuario,Tipo_Producto,Producto
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ['id_usuario','username','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self,validated_data):
        user = Usuario(
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.password = validated_data.get('password',instance.password)
        instance.set_password(instance.password)
        instance.save()
        return instance

class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Producto
        fields = ['id_Tipo','nombre']


class ProductoSerializer(serializers.ModelSerializer):
    tipo =  TipoSerializer(many=True,read_only=True)
    class Meta:
        model = Producto
        fields = ['id_producto','nombre','cantidad','tipo']


