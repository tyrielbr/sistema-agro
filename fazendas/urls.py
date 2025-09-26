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
from django.urls import path
from .views import (
    dashboard, cria_pessoa, cria_fazenda, cria_arrendamento, lista_propriedades, detalhes_propriedade, detalhes_area, cria_area, cria_talhao,
    PessoaUpdateView, PessoaDeleteView, FazendaUpdateView, FazendaDeleteView,
    ArrendamentoUpdateView, ArrendamentoDeleteView, AreaUpdateView, AreaDeleteView, TalhaoUpdateView, TalhaoDeleteView
)

urlpatterns = [
    path('', dashboard, name='fazendas_dashboard'),
    path('pessoa/criar/', cria_pessoa, name='cria_pessoa'),
    path('pessoa/editar/<int:pk>/', PessoaUpdateView.as_view(), name='edita_pessoa'),
    path('pessoa/deletar/<int:pk>/', PessoaDeleteView.as_view(), name='deleta_pessoa'),
    path('fazenda/criar/', cria_fazenda, name='cria_fazenda'),
    path('fazenda/editar/<int:pk>/', FazendaUpdateView.as_view(), name='edita_fazenda'),
    path('fazenda/deletar/<int:pk>/', FazendaDeleteView.as_view(), name='deleta_fazenda'),
    path('arrendamento/criar/', cria_arrendamento, name='cria_arrendamento'),
    path('arrendamento/editar/<int:pk>/', ArrendamentoUpdateView.as_view(), name='edita_arrendamento'),
    path('arrendamento/deletar/<int:pk>/', ArrendamentoDeleteView.as_view(), name='deleta_arrendamento'),
    path('propriedades/', lista_propriedades, name='lista_propriedades'),
    path('propriedade/<str:tipo>/<int:id>/', detalhes_propriedade, name='detalhes_propriedade'),
    path('area/<int:id>/', detalhes_area, name='detalhes_area'),
    path('area/criar/', cria_area, name='cria_area'),
    path('area/editar/<int:pk>/', AreaUpdateView.as_view(), name='edita_area'),
    path('area/deletar/<int:pk>/', AreaDeleteView.as_view(), name='deleta_area'),
    path('talhao/criar/', cria_talhao, name='cria_talhao'),
    path('talhao/editar/<int:pk>/', TalhaoUpdateView.as_view(), name='edita_talhao'),
    path('talhao/deletar/<int:pk>/', TalhaoDeleteView.as_view(), name='deleta_talhao'),
]