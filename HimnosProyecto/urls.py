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
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

urlpatterns: list[URLPattern | URLResolver] = [
    path(route='', view=include('home.urls'), name='home'),
    path(route='admin/', view=admin.site.urls),
    path(route='himnos/', view=include('apiHimnos.urls')),
    path(route='biblia/', view=include('apiBiblia.urls')),
    path(route='administrador/', view=include('apiAdmin.urls')),
]
