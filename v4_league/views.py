from django.shortcuts import render, get_object_or_404
from .models import League


# Create your views here.

def show_league_page(request, league_id):
    league = get_object_or_404(League, id=league_id)
    return render(request, 'v4_league/league_page.html', {'league': league})
