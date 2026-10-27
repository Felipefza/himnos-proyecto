from django.contrib.auth.models import AbstractUser
from django.db.models import AutoField

# Create your models here.

class Administrador(AbstractUser):
    id = AutoField(primary_key=True)
