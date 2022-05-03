from django.db import models

from django.contrib.auth.models import BaseUserManager

'''en esta clase se modifica todo lo que se necesite para crear un usuario, por ejemplo: a la hora de crear
un superusuario, obligamos que se pidiese un email en el momento de crearse.'''
class UserManager(BaseUserManager, models.Manager):

    #aqui es donde se pasan los parametros con los que se creara un superusuario o un superusuario
    ''' esta funcion decide como crear los superusuarios segun los parametros que le enviemos por ejemplo:
    los usuarios normales tienen en su return dos False, es decir que no seran staff ni superusuarios  '''
    def _create_user(self, username, email, password, is_staff, is_superuser,is_active, **extra_fields):
        user = self.model(
            username=username,
            email = email,
            is_staff=is_staff,
            is_superuser= is_superuser,
            is_active = is_active,
            **extra_fields
        )
        #encriptando el password
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True,True, **extra_fields)

    #validacion del codigo de verificacion, saber si existe y si el usuario tambien
    def cod_validation(self, id_user, cod_registro):
        if self.filter(id=id_user, coderegistro=cod_registro).exists():
            return True
        else:
            return False