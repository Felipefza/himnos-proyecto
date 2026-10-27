"""
URL configuration for HimnosProyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import URLPattern, URLResolver, path

from apiBiblia.views import (
    listarBiblia,
    mostrarCapitulo,
    mostrarRangoVersiculos,
    mostrarVersiculos,
    obtenerLibros,
)

urlpatterns: list[URLPattern | URLResolver] = [
    path(route='', view=listarBiblia, name='ApiBiblia_listarBiblia'),
    path(route='libros/', view=obtenerLibros, name='ApiBiblia_obtenerLibros'),
    path(route='palabra/<int:numeroLibro>/<int:numeroCapitulo>', view=mostrarCapitulo, name='ApiBiblia_mostrarCapitulo'),
    path(route='palabra/<int:numeroLibro>/<int:numeroCapitulo>/<int:numeroVersiculo>/', view=mostrarVersiculos, name='ApiBiblia_mostrarVersiculos'),
    path(route='palabra/<int:numeroLibro>/<int:numeroCapitulo>/<int:versiculoComienzo>/<int:versiculoFin>/', view=mostrarRangoVersiculos, name='ApiBiblia_mostrarRangoVersiculos'),
]
