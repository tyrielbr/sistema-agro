from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Insumo
from fiscal.models import NfRecebida

@login_required
def dashboard(request):
    granel = Insumo.objects.filter(categoria='granel', owner=request.user) if not request.user.is_superuser else Insumo.objects.filter(categoria='granel')
    lavoura = Insumo.objects.filter(categoria='lavoura', owner=request.user) if not request.user.is_superuser else Insumo.objects.filter(categoria='lavoura')
    maquinas = Insumo.objects.filter(categoria='maquinas', owner=request.user) if not request.user.is_superuser else Insumo.objects.filter(categoria='maquinas')
    context = {'granel': granel, 'lavoura': lavoura, 'maquinas': maquinas}
    return render(request, 'estoque/dashboard.html', context)