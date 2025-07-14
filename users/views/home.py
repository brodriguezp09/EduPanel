from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """
    Vista para la página de inicio del usuario autenticado.
    """
    context = {
        'user': request.user
    }
    return render(request, 'home.html', context)