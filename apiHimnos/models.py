from django.db import models
from django.db.models import (
    CASCADE,
    AutoField,
    DateField,
    ForeignKey,
    IntegerField,
    TextField,
)

# Create your models here.

class Himnos(models.Model):
    himno_id = AutoField(primary_key=True)
    titulo = TextField()
    numero = IntegerField()

    objects: models.Manager = models.Manager()

    def __str__(self):
        return (
            f"\nID:           {self.himno_id}"
            f"\nTitulo:       {self.titulo}"
            f"\nNumero:       {self.numero}"
        )

class Parrafos(models.Model):
    parrafo_id= AutoField(primary_key=True)
    parrafo = TextField()
    numero_parrafo = IntegerField()
    himno_id_fk = ForeignKey(to=Himnos, on_delete=CASCADE)

    objects: models.Manager = models.Manager()

    def __str__(self):
        return (
            f"\nID:                 {self.parrafo_id}"
            f"\nParrafo:            {self.parrafo}"
            f"\nNumero Parrafo:     {self.numero_parrafo}"
            f"\nHimno ID:           {self.himno_id_fk}"
        )

class ParrafoCoros(models.Model):
    parrafo_coro_id = AutoField(primary_key=True)
    parrafo = TextField()
    numero_parrafo = IntegerField()
    himno_id_fk = ForeignKey(to=Himnos, on_delete=CASCADE)

    objects: models.Manager = models.Manager()

    def __str__(self):
        return (
            f"\nID:                 {self.parrafo_coro_id}"
            f"\nParrafo:            {self.parrafo}"
            f"\nNumero Parrafo:     {self.numero_parrafo}"
            f"\nHimno ID:           {self.himno_id_fk}"
        )

class HimnosActivo(models.Model):
    id = models.AutoField(primary_key=True)
    himno_id_fk = ForeignKey(to=Himnos, on_delete=CASCADE)

    objects: models.Manager = models.Manager()

class HistorialHimnosActivos(models.Model):
    id = models.AutoField(primary_key=True)
    historial_himno_id_fk = ForeignKey(to=Himnos, on_delete=CASCADE)
    historial_fecha = DateField(auto_now_add=True)
