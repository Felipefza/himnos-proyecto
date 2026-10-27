from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from static.scripts.biblia import Biblia
from static.scripts.busqueda import BusquedaFuzz

from .models import Versiculos, VersiculosActivos

# Create your views here.

biblia: Biblia = Biblia()
busqueda: BusquedaFuzz = BusquedaFuzz()


def obtenerLibros(request: HttpRequest) -> HttpResponse:
    datos: dict[str, Any] = {
        'librosNuevoTestamento': [],
        'librosAntiguoTestamento': [],
    }

    libroABuscar: str | None = request.GET.get(key='libro', default=None)

    versiculoActivo: VersiculosActivos | None = VersiculosActivos.objects.first()
    datos['versiculoActivos'] = versiculoActivo

    cantidadCapitulos: int

    if libroABuscar:
        datosAntiguoTestamento: list[dict[str, Any]] = busqueda.buscarLibros(diccionario_libros=biblia.ANTIGUO_TESTAMENTO, palabra=libroABuscar)
        datosNuevoTestamento: list[dict[str, Any]] = busqueda.buscarLibros(diccionario_libros=biblia.NUEVO_TESTAMENTO, palabra=libroABuscar)

        index: int
        nombreLibro: str
        ultimoCapitulo: Versiculos | None

        for item in datosAntiguoTestamento:
            index = item['index']
            nombreLibro = item['nombreLibro']

            ultimoCapitulo = Versiculos.objects.filter(libro=index).distinct().last()

            if ultimoCapitulo:
                cantidadCapitulos = int(ultimoCapitulo.capitulo)

                datos['librosAntiguoTestamento'].append({
                    'index': index,
                    'nombreLibro': nombreLibro,
                    'cantidadCapitulos': [cantidad for cantidad in range(1, cantidadCapitulos + 1)]
                })


        for item in datosNuevoTestamento:
            index = item['index']
            nombreLibro = item['nombreLibro']

            ultimoCapitulo = Versiculos.objects.filter(libro=index).distinct().last()

            if ultimoCapitulo:
                cantidadCapitulos = int(ultimoCapitulo.capitulo)

                datos['librosNuevoTestamento'].append({
                    'index': index,
                    'nombreLibro': nombreLibro,
                    'cantidadCapitulos': [cantidad for cantidad in range(1, cantidadCapitulos + 1)]
                })
    else:
        for index, nombreLibro in biblia.ANTIGUO_TESTAMENTO.items():
            ultimoCapitulo = Versiculos.objects.filter(libro=index).distinct().last()

            if ultimoCapitulo:
                cantidadCapitulos = int(ultimoCapitulo.capitulo)

                datos['librosAntiguoTestamento'].append({
                    'index': index,
                    'nombreLibro': nombreLibro,
                    'cantidadCapitulos': [cantidad for cantidad in range(1, cantidadCapitulos + 1)]
                })

        for index, nombreLibro in biblia.NUEVO_TESTAMENTO.items():
            ultimoCapitulo = Versiculos.objects.filter(libro=index).distinct().last()

            if ultimoCapitulo:
                cantidadCapitulos = int(ultimoCapitulo.capitulo)

                datos['librosNuevoTestamento'].append({
                    'index': index,
                    'nombreLibro': nombreLibro,
                    'cantidadCapitulos': [cantidad for cantidad in range(1, cantidadCapitulos + 1)]
                })


    # datos = {
    #     'librosAntiguoTestamento': [
    #         {
    #             'nombreLibro': 'genesis',
    #             'cantidadCapitulos': [index for index in range(11)]
    #         }
    #     ],
    #     'librosNuevoTestamento': [
    #         {
    #             'nombreLibro': 'leviticos',
    #             'cantidadCapitulos': [index for index in range(11)]
    #         }
    #     ],
    # }

    return render(request=request, template_name='apiBiblia/resultadosDinamicosBiblia.html', context=datos)


def listarBiblia(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='apiBiblia/listarBiblia.html')


def mostrarVersiculos(request: HttpRequest, numeroLibro: int, numeroCapitulo: int, numeroVersiculo: int) -> HttpResponse:
    listaVersiculos: list[Versiculos] = []

    libro: str | None = biblia.NOMBRES_LIBROS[numeroLibro]

    versiculo: Versiculos | None = Versiculos.objects.get(libro=numeroLibro, capitulo=numeroCapitulo, versiculo=numeroVersiculo)
    capAnterior: Versiculos | None = capituloAnterior(numeroLibro=numeroLibro, numeroCapitulo=numeroCapitulo)
    capSiguiente: Versiculos | None = capituloSiguiente(numeroLibro=numeroLibro, numeroCapitulo=numeroCapitulo)

    if versiculo:
        listaVersiculos.append(versiculo)

    datos: dict[str, Any] = {
        'listaVersiculos': listaVersiculos,
        'libroNombre': libro,
        'numeroCapitulo': numeroCapitulo,
        'numeroVersiculo': numeroVersiculo,
        'back': capAnterior,
        'next': capSiguiente,
    }

    return render(request=request, template_name='apiBiblia/mostrarVersiculos.html', context=datos)


def mostrarRangoVersiculos(request: HttpRequest, numeroLibro: int, numeroCapitulo: int, versiculoComienzo: int, versiculoFin: int) -> HttpResponse:
    listaVersiculos: list[Versiculos] = []

    libro: str | None = biblia.NOMBRES_LIBROS[numeroLibro]

    for index in range(versiculoComienzo, versiculoFin + 1):
        versiculo: Versiculos | None = Versiculos.objects.get(libro=numeroLibro, capitulo=numeroCapitulo, versiculo=index)
        if versiculo:
            listaVersiculos.append(versiculo)

    capAnterior: Versiculos | None = capituloAnterior(numeroLibro=numeroLibro, numeroCapitulo=numeroCapitulo)
    capSiguiente: Versiculos | None = capituloSiguiente(numeroLibro=numeroLibro, numeroCapitulo=numeroCapitulo)

    datos: dict[str, Any] = {
        'listaVersiculos': listaVersiculos,
        'libroNombre': libro,
        'numeroCapitulo': numeroCapitulo,
        'versiculoComienzo': versiculoComienzo,
        'versiculoFin': versiculoFin,
        'back': capAnterior,
        'next': capSiguiente,
    }

    return render(request=request, template_name='apiBiblia/mostrarVersiculos.html', context=datos)


def mostrarCapitulo(request: HttpRequest, numeroLibro: int, numeroCapitulo: int) -> HttpResponse:
    libro: str | None = biblia.NOMBRES_LIBROS[numeroLibro]

    versiculos: QuerySet[Versiculos] = Versiculos.objects.filter(libro=numeroLibro, capitulo=numeroCapitulo)
    capAnterior: Versiculos | None = capituloAnterior(numeroLibro=numeroLibro, numeroCapitulo=numeroCapitulo)
    capSiguiente: Versiculos | None = capituloSiguiente(numeroLibro=numeroLibro, numeroCapitulo=numeroCapitulo)

    datos: dict[str, Any] = {
        'listaVersiculos': versiculos,
        'libroNombre': libro,
        'numeroCapitulo': numeroCapitulo,
        'back': capAnterior,
        'next': capSiguiente,
    }

    return render(request=request, template_name='apiBiblia/mostrarVersiculos.html', context=datos)

def capituloAnterior(numeroLibro: int, numeroCapitulo: int) -> Versiculos | None:
    if numeroCapitulo == 1:
        siHayAnteriorLibro: QuerySet[Versiculos] | None = Versiculos.objects.filter(libro=numeroLibro - 1)

        if siHayAnteriorLibro:
            ultimoCapitulo: Versiculos | None = Versiculos.objects.filter(libro=numeroLibro - 1).distinct().last()
            if ultimoCapitulo:
                return Versiculos.objects.filter(libro=numeroLibro - 1, capitulo=ultimoCapitulo.capitulo).first()

    else:
        return Versiculos.objects.filter(libro=numeroLibro, capitulo=numeroCapitulo - 1).first()

    return None

def capituloSiguiente(numeroLibro: int, numeroCapitulo: int) -> Versiculos | None:
    capituloActual: Versiculos | None = Versiculos.objects.filter(libro=numeroLibro, capitulo=numeroCapitulo).last()
    capituloUltimo: Versiculos | None = Versiculos.objects.filter(libro=numeroLibro).last()

    siguienteCapitulo: Versiculos | None

    if capituloActual == capituloUltimo:
        siguienteCapitulo = Versiculos.objects.filter(libro=numeroLibro + 1, capitulo=1).first()
        if siguienteCapitulo:
            return siguienteCapitulo
    else:
        siguienteCapitulo = Versiculos.objects.filter(libro=numeroLibro, capitulo=numeroCapitulo + 1).first()
        return siguienteCapitulo

    return None


def obtenerCantidadCapitulos(request: HttpRequest, nombreLibro: str) -> JsonResponse:
    datos = {}

    try:
        cantidad: int = Versiculos.objects.filter(nombreLibro=nombreLibro, versiculo=1).count()

        datos['cantidadVersiculos'] = cantidad

    except ObjectDoesNotExist:
        datos['cantidadVersiculos'] = 0

    return JsonResponse(data=datos)


def obtenerCantidadVersiculos(request: HttpRequest, nombreLibro: str, numeroCapitulo: int) -> JsonResponse:
    datos = {}

    try:
        cantidad: int = Versiculos.objects.filter(nombreLibro=nombreLibro, capitulo=numeroCapitulo).count()

        datos['cantidadVersiculos'] = cantidad

    except ObjectDoesNotExist:
        datos['cantidadVersiculos'] = 0

    return JsonResponse(data=datos)
