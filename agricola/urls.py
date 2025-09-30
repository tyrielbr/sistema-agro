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
from .views import dashboard, lista_ordens, cria_ordem, aprova_ordem, ordens_realizadas, ordens_planejadas, lavouras_ativas, historico_produtividade, cria_lavoura, lista_lavouras, remove_lavoura, gerenciar_culturas

urlpatterns = [
    path('', dashboard, name='agricola_dashboard'),
    path('ordens/', lista_ordens, name='lista_ordens'),
    path('ordens/criar/', cria_ordem, name='cria_ordem'),
    path('ordens/<int:ordem_id>/aprovar/', aprova_ordem, name='aprova_ordem'),
    path('ordens/realizadas/', ordens_realizadas, name='ordens_realizadas'),
    path('ordens/planejadas/', ordens_planejadas, name='ordens_planejadas'),
    path('lavouras/ativas/', lavouras_ativas, name='lavouras_ativas'),
    path('produtividade/historico/', historico_produtividade, name='historico_produtividade'),
    path('lavouras/criar/', cria_lavoura, name='cria_lavoura'),
    path('lavouras/', lista_lavouras, name='lista_lavouras'),
    path('lavouras/<int:lavoura_id>/remover/', remove_lavoura, name='remove_lavoura'),
    path('culturas/gerenciar/', gerenciar_culturas, name='gerenciar_culturas'),
    path('ordens/planejar/<int:ordem_id>/', ordens_planejadas, name='planejar_ordem'),
    path('ordens/filtrar/', lista_ordens, name='filtrar_ordens'),
]