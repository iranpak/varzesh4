from django.shortcuts import render


# Create your views here.

def show_league_page(request):
    return render(request, 'v4_league/league_page.html')
