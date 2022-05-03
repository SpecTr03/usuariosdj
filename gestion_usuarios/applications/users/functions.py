# Funciones extra de la aplicacion users

import random
import string

#creando un codigo aleatorio para la verificacion de email de un usuario que se registre
def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

