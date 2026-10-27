from typing import Any

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import ObjectDoesNotExist, QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from apiBiblia.models import Versiculos, VersiculosActivos
from apiHimnos.models import Himnos, HimnosActivo, ParrafoCoros, Parrafos
from HimnosProyecto import settings
from static.scripts.busqueda import BusquedaFuzz


fuzz: BusquedaFuzz = BusquedaFuzz()

# Create your views here.

@login_required(login_url='/administrador/')
def obtenerHimnos(request: HttpRequest) -> HttpResponse:
  himnos: QuerySet[Himnos] = Himnos.objects.all()
  himnos = himnos.order_by('numero')

  himnoActivo: QuerySet[HimnosActivo] | None = HimnosActivo.objects.first()

  if himnoActivo:
    himnos = himnos.exclude(himno_id=himnoActivo.himno_id_fk.himno_id)
    himnoActivo = Himnos.objects.get(himno_id=himnoActivo.himno_id_fk.himno_id)

  himnosDatos: list[Any] = list(himnos.values())

  datos = {
      'himnos': himnosDatos,
      'himnoActivo': himnoActivo,
      'himno_url': 'administrador'
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
      template_name='apiAdmin/resultadosDinamicosHimnos.html',
      context=datos
  )


@login_required(login_url='/administrador/')
def listarHimnos(request: HttpRequest) -> HttpResponse:
    opcionesOrdenar: dict[str, str] = {
        'numeroAscendente': 'Ordenar por Número (Ascendente)',
        'numeroDescendente': 'Ordenar por Número (Descendente)',
        'tituloAscendente': 'Ordenar por Titulo (Ascendente)',
        'tituloDescendente': 'Ordenar por Titulo (Descendente)',
    }

    datos = {
        'opciones': opcionesOrdenar,
        'obtenerHimnos_url': 'ApiAdmin_obtenerHimnos',
    }

    return render(
        request=request,
        template_name='apiAdmin/listarHimnos.html',
        context=datos
    )


@login_required(login_url='/administrador/')
def opcionesHimno(request: HttpRequest, himno_id: int) -> HttpResponse:
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

  activo: HimnosActivo | None = HimnosActivo.objects.first()
  esActivo: HimnosActivo | None

  try:
    esActivo = HimnosActivo.objects.get(himno_id_fk=himno_id)
  except ObjectDoesNotExist:
    esActivo = None

  datos = {
      'himno': himno,
      'parrafos': listaParrafosOrdenada,
      'coros_ids': coros_ids,
      'activo': activo,
      'esActivo': esActivo,
  }

  return render(request=request, template_name='apiAdmin/opciones.html', context=datos)


@login_required(login_url='/administrador/')
def eliminarHimno(request: HttpRequest, himno_id: int) -> HttpResponse:
    himno: Himnos = Himnos.objects.get(himno_id=himno_id)
    himno.delete()

    return redirect(to='ApiAdmin_listarHimnos')


@login_required(login_url='/administrador/')
def activarHimno(request: HttpRequest, himno_id: int) -> HttpResponse:
  existe: QuerySet[HimnosActivo] | None = HimnosActivo.objects.first()

  if not existe:
    himno: QuerySet[Himnos] = Himnos.objects.get(himno_id=himno_id)
    himnoActivo: HimnosActivo = HimnosActivo(himno_id_fk=himno)
    himnoActivo.save()

  return redirect('ApiAdmin_listarHimnos')


@login_required(login_url='/administrador/')
def desactivarHimno(request: HttpRequest, himno_id: int) -> HttpResponse:
  existe: QuerySet[HimnosActivo] | None = HimnosActivo.objects.get(himno_id_fk=himno_id)

  if existe:
    existe.delete()

  return redirect('ApiAdmin_listarHimnos')


@login_required(login_url='/administrador/')
def agregarHimno(request: HttpRequest) -> HttpResponse:
    datos = {}

    if request.method == 'POST':
        try:
            numero: str | None = request.POST.get('numero')
            titulo: str | None = request.POST.get('titulo')

            opcionParrafo: list[str] | None = request.POST.getlist('opcionParrafo')
            textoParrafos: list[str] | None = request.POST.getlist('textoParrafo')

            himno: Himnos = Himnos(numero=numero, titulo=titulo)
            himno.save()

            index: int = 1

            for parrafo, opcion in zip(textoParrafos, opcionParrafo):
                result: Parrafos | ParrafoCoros

                if opcion == 'parrafo':
                    result = Parrafos(parrafo=parrafo, numero_parrafo=index, himno_id_fk=himno)
                else:
                    result = ParrafoCoros(parrafo=parrafo, numero_parrafo=index, himno_id_fk=himno)

                result.save()
                index += 1

            return redirect('ApiAdmin_listarHimnos')

        except ValueError:
            ...

    return render(request=request, template_name='apiAdmin/agregarHimno.html', context=datos)


@login_required(login_url='/administrador/')
def modificarHimno(request: HttpRequest, himno_id: int) -> HttpResponse:
    if request.method == 'POST':
        try:
            numero: str | None = request.POST.get('numero')
            titulo: str | None = request.POST.get('titulo')

            opcionParrafo: list[str] | None = request.POST.getlist('opcionParrafo')
            textoParrafos: list[str] | None = request.POST.getlist('textoParrafo')

            if not numero or not titulo or not opcionParrafo or not textoParrafos:
                raise ValueError

            # ELiminar El Himno Y despues crearlo de nuevo
            himnoEliminar: Himnos = Himnos.objects.get(himno_id=himno_id)
            himnoEliminar.delete()

            parrafosEliminar: QuerySet[Parrafos] = Parrafos.objects.filter(himno_id_fk=himno_id)
            parrafoCorosEliminar: QuerySet[Parrafos] = ParrafoCoros.objects.filter(himno_id_fk=himno_id)

            for item in parrafosEliminar:
                item.delete()

            for item in parrafoCorosEliminar:
                item.delete()

            himnoMod: Himnos = Himnos(numero=numero, titulo=titulo)
            himnoMod.save()

            index: int = 1

            for parrafo, opcion in zip(textoParrafos, opcionParrafo):
                result: Parrafos | ParrafoCoros

                if opcion == 'parrafo':
                    result = Parrafos(parrafo=parrafo, numero_parrafo=index, himno_id_fk=himnoMod)
                else:
                    result = ParrafoCoros(parrafo=parrafo, numero_parrafo=index, himno_id_fk=himnoMod)

                result.save()
                index += 1

            return redirect('ApiAdmin_listarHimnos')

        except ValueError, ObjectDoesNotExist:
            ...

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

    return render(request=request, template_name='apiAdmin/modificarHimno.html', context=datos)


def autentificacion(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('ApiAdmin_listarHimnos')

    if request.method == "GET":
        usuario: str | None = request.GET.get('usuario')
        contrasena: str | None = request.GET.get('contrasena')

        user: object | None = authenticate(request=request, username=usuario, password=contrasena)

        if user is not None:
            login(request=request, user=user)
            return redirect('ApiAdmin_listarHimnos')

    return render(request=request, template_name="apiAdmin/autentificacion.html")


@login_required(login_url='/administrador/')
def logoutAdmin(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect('home')


def obtenerCantidadCapitulos(request: HttpRequest, nombreLibro: str) -> JsonResponse:
    datos = {}

    try:
        cantidad: int = Versiculos.objects.filter(nombreLibro=nombreLibro, versiculo=1).count()

        datos['cantidadCapitulos'] = cantidad

    except ObjectDoesNotExist:
        datos['cantidadCapitulos'] = 0

    return JsonResponse(data=datos)


def obtenerCantidadVersiculos(request: HttpRequest, nombreLibro: str, numeroCapitulo: int) -> JsonResponse:
    datos = {}

    try:
        cantidad: int = Versiculos.objects.filter(nombreLibro=nombreLibro, capitulo=numeroCapitulo).count()

        datos['cantidadVersiculos'] = cantidad

    except ObjectDoesNotExist:
        datos['cantidadVersiculos'] = 0

    return JsonResponse(data=datos)


def agregarVersiculosActivos(request: HttpRequest, ) -> HttpResponse:
    datos = {}

    nombreLibros: QuerySet[Versiculos] = Versiculos.objects.filter(capitulo=1, versiculo=1)
    datos['libros'] = nombreLibros

    versiculoActivoActual: VersiculosActivos | None = VersiculosActivos.objects.first()

    if versiculoActivoActual is None:
        datos['hayVersiculoActivo'] = False

        datos['versiculoActivo'] = {
            'versiculos_activos_comienzo_fk': {
                'libro': 1,
                'capitulo': 1,
                'versiculo': 1,
                'nombreLibro': 'Génesis',
            },
            'versiculos_activos_fin_fk': {
                'libro': 1,
                'capitulo': 1,
                'versiculo': 2,
                'nombreLibro': 'Génesis',
            }
        }

    else:
        datos['hayVersiculoActivo'] = True

        datos['versiculoActivo'] = versiculoActivoActual

    versiculoAEliminar: QuerySet[VersiculosActivos] | None

    nombreLibro: str | None = request.POST.get(key='nombreLibro', default=None)
    numeroCapitulo: str | None = request.POST.get(key='numeroCapitulo', default=None)
    numeroVersiculoComienzo: str | None = request.POST.get(key='numeroVersiculoComienzo', default=None)
    numeroVersiculoFin: str | None = request.POST.get(key='numeroVersiculoFin', default=None)

    if request.method == 'POST':
        numeroCapituloInt: int
        numeroVersiculoComienzoInt: int
        numeroVersiculoFinInt: int

        if numeroCapitulo and numeroVersiculoComienzo and numeroVersiculoFin:
            numeroCapituloInt = int(numeroCapitulo)
            numeroVersiculoComienzoInt = int(numeroVersiculoComienzo)
            numeroVersiculoFinInt = int(numeroVersiculoFin)
        else:
            return render(request=request, template_name='apiAdmin/opcionesBiblia.html', context=datos)

        versiculosComienzo: Versiculos | None = Versiculos.objects.get(nombreLibro=nombreLibro, capitulo=numeroCapituloInt, versiculo=numeroVersiculoComienzoInt)
        versiculosFin: Versiculos | None = Versiculos.objects.get(nombreLibro=nombreLibro, capitulo=numeroCapituloInt, versiculo=numeroVersiculoFinInt)

        if versiculosComienzo and versiculosFin:
            if versiculosComienzo.versiculo > versiculosFin.versiculo:
                return render(request=request, template_name='apiAdmin/opcionesBiblia.html', context=datos)

            versiculoAEliminar = VersiculosActivos.objects.all()

            if versiculoAEliminar:
                versiculoAEliminar.delete()

            versiculosActivos: VersiculosActivos = VersiculosActivos(versiculos_activos_comienzo_fk=versiculosComienzo, versiculos_activos_fin_fk=versiculosFin)
            versiculosActivos.save()

        return redirect('ApiAdmin_opcionesBiblia')


    return render(request=request, template_name='apiAdmin/opcionesBiblia.html', context=datos)


def desactivarVersiculosActivos(request: HttpRequest) -> HttpResponse:
    versiculoAEliminar = VersiculosActivos.objects.all()

    if versiculoAEliminar:
        versiculoAEliminar.delete()

    return redirect('ApiAdmin_opcionesBiblia')
