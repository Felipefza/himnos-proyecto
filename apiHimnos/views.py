from typing import Any

from django.db.models import ObjectDoesNotExist, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from static.scripts.busqueda import BusquedaFuzz

from .models import Himnos, HimnosActivo, ParrafoCoros, Parrafos

fuzz: BusquedaFuzz = BusquedaFuzz()

# Create your views here.

def obtenerHimnos(request: HttpRequest) -> HttpResponse:
  himnos: QuerySet[Himnos] = Himnos.objects.all()
  himnos = himnos.order_by('numero')

  himnoActivo: QuerySet[Himnos] | None | QuerySet[HimnosActivo] = HimnosActivo.objects.first()

  if himnoActivo:
    himnos = himnos.exclude(himno_id=himnoActivo.himno_id_fk.himno_id)
    himnoActivo = Himnos.objects.get(himno_id=himnoActivo.himno_id_fk.himno_id)

  himnosDatos: list[Any] = list(himnos.values())

  datos = {
      'himnos': himnosDatos,
      'himnoActivo': himnoActivo,
      'himno_url': 'himnos'
  }

  numero: object | list[object] | None = request.GET.get(key="numero", default=None)
  titulo: object | list[object] | None = request.GET.get(key="titulo", default=None)
  letra: object | list[object] | None = request.GET.get(key="letra", default=None)
  ordenar: object | list[object] | None = request.GET.get(key="ordenar", default=None)

  if numero:
      datos['himnos'] = fuzz.buscarNumero(lista_himnos=datos['himnos'], palabra=str(numero))

  if titulo:
      datos['himnos'] = fuzz.buscarTitulo(lista_himnos=datos['himnos'], palabra=str(titulo))

  if letra:
      tempHimnos: list[Any] = datos['himnos'].copy()
      for item in datos['himnos']:
          parrafos: QuerySet[Parrafos] = Parrafos.objects.filter(himno_id_fk=item['himno_id'])
          lista_parrafos: list[Any] = list(parrafos.values_list())
          resultado: bool = fuzz.buscarLetra(lista_parrafos=lista_parrafos, palabra=str(letra))

          if not resultado:
              try:
                  parrafoCoros: QuerySet[ParrafoCoros] = ParrafoCoros.objects.filter(himno_id_fk=item['himno_id'])
                  lista_parrafoCoros: list[Any] = list(parrafoCoros.values_list())
                  resultado = fuzz.buscarLetra(lista_parrafos=lista_parrafoCoros, palabra=str(letra))
              except ObjectDoesNotExist:
                  ...

          if not resultado:
              tempHimnos.remove(item)

      datos['himnos'] = tempHimnos

  if ordenar:
      match ordenar:
          case 'numeroAscendente':
              datos['himnos'] = sorted(datos['himnos'], key=lambda d: d['numero'])
          case 'numeroDescendente':
              datos['himnos'] = sorted(datos['himnos'], key=lambda d: d['numero'], reverse=True)
          case 'tituloAscendente':
              datos['himnos'] = sorted(datos['himnos'], key=lambda d: d['titulo'])
          case 'tituloDescendente':
              datos['himnos'] = sorted(datos['himnos'], key=lambda d: d['titulo'], reverse=True)


  return render(
      request=request,
      template_name='apiHimnos/resultadosDinamicosHimnos.html',
      context=datos
  )


def listarHimnos(request: HttpRequest) -> HttpResponse:
    opcionesOrdenar: dict[str, str] = {
        'numeroAscendente': 'Ordenar por Número (Ascendente)',
        'numeroDescendente': 'Ordenar por Número (Descendente)',
        'tituloAscendente': 'Ordenar por Titulo (Ascendente)',
        'tituloDescendente': 'Ordenar por Titulo (Descendente)',
    }

    datos = {
        'opciones': opcionesOrdenar,
        'obtenerHimnos_url': 'ApiHimnos_obtenerHimnos',
    }

    return render(
        request=request,
        template_name='apiHimnos/listarHimnos.html',
        context=datos
    )


def mostrarHimno(request: HttpRequest, himno_id: int) -> HttpResponse:
    himno: Himnos = Himnos.objects.get(himno_id=himno_id)
    parrafos: QuerySet[Parrafos] = Parrafos.objects.filter(himno_id_fk=himno_id)
    parrafoCoro: QuerySet[ParrafoCoros] = ParrafoCoros.objects.filter(himno_id_fk=himno_id)

    coros_ids: list[Any] = list(parrafoCoro.values_list('numero_parrafo', flat=True))

    listaParrafos = list(parrafos.values())
    listaParrafoCoro = list(parrafoCoro.values())

    listaParrafos.extend(listaParrafoCoro)

    listaParrafosOrdenada = sorted(listaParrafos, key=lambda d: d['numero_parrafo'])

    parrafoIndex: int = 1

    for index, item in enumerate(listaParrafosOrdenada):
        if not (index + 1) in coros_ids:
            item['index'] = parrafoIndex
            parrafoIndex += 1

    datos = {
        'himno': himno,
        'parrafos': listaParrafosOrdenada,
        'coros_ids': coros_ids,
    }

    return render(
        request=request,
        template_name='apiHimnos/himno.html',
        context=datos
    )
