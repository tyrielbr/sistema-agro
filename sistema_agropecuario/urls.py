"""
URL configuration for sistema_agropecuario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from .views import fluxogramas, home

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('fazendas/', include('fazendas.urls')),
    path('agricola/', include('agricola.urls')),
    path('estoque/', include('estoque.urls')),
    path('administrativo/', include('administrativo.urls')),
    path('maquinas/', include('maquinas.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('comercial/', include('comercial.urls')),
    path('dashboard-master/', include('dashboard_master.urls')),
    path('fluxogramas/', fluxogramas, name='fluxogramas'),
]