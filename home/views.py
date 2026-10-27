from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apiBiblia.models import Versiculos, VersiculosActivos
from apiHimnos.models import Himnos, HimnosActivo

# Create your views here.


def home(request: HttpRequest) -> HttpResponse:
    himnoActivo: HimnosActivo | None = HimnosActivo.objects.first()
    versiculosActivos: VersiculosActivos | None = VersiculosActivos.objects.first()


    datos = {
        'himnoActivo': himnoActivo,
        'versiculosActivos': versiculosActivos,
    }

    return render(
        request=request,
        template_name="home/index.html",
        context=datos
    )
