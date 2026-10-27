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

from .views import (
    activarHimno,
    agregarHimno,
    agregarVersiculosActivos,
    autentificacion,
    desactivarHimno,
    desactivarVersiculosActivos,
    eliminarHimno,
    listarHimnos,
    logoutAdmin,
    modificarHimno,
    obtenerCantidadCapitulos,
    obtenerCantidadVersiculos,
    obtenerHimnos,
    opcionesHimno,
)

urlpatterns: list[URLPattern | URLResolver] = [
    path(route='', view=autentificacion, name='ApiAdmin_autentificacion'),
    path(route='listarHimnos/', view=listarHimnos, name='ApiAdmin_listarHimnos'),
    path(route='obtenerHimnos/', view=obtenerHimnos, name='ApiAdmin_obtenerHimnos'),
    path(route='<int:himno_id>/', view=opcionesHimno, name='ApiAdmin_opcionesHimno'),
    path(route='agregar/', view=agregarHimno, name='ApiAdmin_agregar'),
    path(route='modificar/<int:himno_id>/', view=modificarHimno, name='ApiAdmin_modificar'),
    path(route='eliminar/<int:himno_id>/', view=eliminarHimno, name='ApiAdmin_eliminar'),
    path(route='activarHimno/<int:himno_id>/', view=activarHimno, name='ApiAdmin_activarHimno'),
    path(route='desactivarHimno/<int:himno_id>/', view=desactivarHimno, name='ApiAdmin_desactivarHimno'),
    path(route='logout/', view=logoutAdmin, name='ApiAdmin_logout'),

    path(route='opcionesBiblia/', view=agregarVersiculosActivos, name='ApiAdmin_opcionesBiblia'),
    path(route='obtenerCantidadCapitulos/<str:nombreLibro>/', view=obtenerCantidadCapitulos, name='ApiAdmin_obtenerCantidadCapitulos'),
    path(route='obtenerCantidadVersiculos/<str:nombreLibro>/<int:numeroCapitulo>/', view=obtenerCantidadVersiculos, name='ApiAdmin_obtenerCantidadVersiculos'),

    path(route='desactivarVersiculosActivos/', view=desactivarVersiculosActivos, name='ApiAdmin_desactivarVersiculosActivos'),
]
