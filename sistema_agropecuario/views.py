from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'index.html')

def fluxogramas(request):
    fluxograma_geral = """
    graph LR
        A[Fazendas: Áreas/Talhões] --> B[Agrícola: Manejo]
        A --> C[Máquinas/Implementos]
        B --> D[Estoque]
        B --> E[Administrativo: Centros de Custo]
        C --> B
        D --> F[Comercial / NFE]
        F --> G[Financeiro]
        E --> G
        H[Módulo Interface / IA] --> A
        H --> B
        H --> F
        H --> G
        G --> H
    """
    return render(request, 'fluxogramas.html', {'fluxograma_geral': fluxograma_geral})