from django.shortcuts import render

# Create your views here.


def show_homepage(request):
    return render(request, 'v4_player/homepage.html')