
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

class Versiculos(models.Model):
    palabra_id = AutoField(primary_key=True)
    palabra = TextField()
    libro = IntegerField()
    capitulo = IntegerField()
    versiculo = IntegerField()
    nombreLibro = TextField()
    titulo = TextField()

    objects: models.Manager = models.Manager()

    def __str__(self) -> str:
        return (

            f'\n==== ID {self.palabra_id} ===='
            f'\nNumero Libro:       {self.libro}'
            f'\nNumero Capitulo:    {self.capitulo}'
            f'\nNumero Versiculo:   {self.versiculo}'
            f'\nPalabra:            {self.palabra}'
        )

class VersiculosActivos(models.Model):
    id = models.AutoField(primary_key=True)
    versiculos_activos_comienzo_fk = ForeignKey(to=Versiculos, on_delete=CASCADE, related_name='appBiblia_versiculos_activos_comienzo_fk')
    versiculos_activos_fin_fk = ForeignKey(to=Versiculos, on_delete=CASCADE, related_name='appBiblia_versiculos_activos_fin_fk')

    objects: models.Manager = models.Manager()

class HistorialVersiculosActivos(models.Model):
    id = models.AutoField(primary_key=True)
    historial_comienzo_fk = ForeignKey(to=Versiculos, on_delete=CASCADE, related_name='appBiblia_historial_comienzo_fk')
    historial_fin_fk = ForeignKey(to=Versiculos, on_delete=CASCADE, related_name='appBiblia_historial_fin_fk')
    historial_fecha = DateField(auto_now_add=True)

    objects: models.Manager = models.Manager()
