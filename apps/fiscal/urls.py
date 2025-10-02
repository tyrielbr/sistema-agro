
from django.urls import path
from .views import dashboard, detalhes_nf, lancamento_nf, HistoricoListView, atualizar_notas

urlpatterns = [
    path('', dashboard, name='fiscal_dashboard'),
    path('nf/<int:pk>/', detalhes_nf, name='detalhes_nf'),
    path('lancamento/<int:pk>/', lancamento_nf, name='lancamento_nf'),
    path('historico/', HistoricoListView.as_view(), name='fiscal_historico'),
    path('atualizar/', atualizar_notas, name='atualizar_notas'),
]