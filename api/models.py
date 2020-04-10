from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver  
from rest_framework.authtoken.models import Token
# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self,username,password=None):
        if not username:
            raise ValueError('Se requiere nombre de usuario!')
        if not password:
            raise ValueError('Se requerie un password!')
        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,password):
        user = self.create_user(
            username = username,
            password = password,
        )
        user.is_admin= True
        user.is_staff= True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class Usuario(AbstractBaseUser):
    id_usuario      =   models.AutoField(db_column='id_usuario', primary_key=True)
    username        =   models.CharField(max_length=255, unique=True)
    #password       =    models.CharField(max_length=255, blank=True, null=True)
    date_joined     =     models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login      =     models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin        =     models.BooleanField(default=False)
    is_active       =     models.BooleanField(default=True)
    is_staff        =     models.BooleanField(default=False)
    is_superuser    =     models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS= []
    objects = UsuarioManager() 
    
    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Tipo_Producto(models.Model):
    id_Tipo         =   models.AutoField(primary_key=True)
    nombre          =   models.CharField(max_length=255)
    def __str__(self):
        return(self.nombre)

class Producto(models.Model):
    id_producto     =   models.AutoField(primary_key=True)
    nombre          =   models.CharField(max_length=255)
    cantidad        =   models.IntegerField(null=True)
    tipo            =   models.ForeignKey(Tipo_Producto,related_name='tipo_producto',on_delete=models.CASCADE)
    def __str__(self):
        return(self.id_producto,self.nombre,self.cantidad,self.tipo)