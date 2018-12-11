from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def show_main_page(request):
    return render(request, 'v4_main/homepage.html')

