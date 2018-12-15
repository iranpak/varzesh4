from django.shortcuts import render

# Create your views here.


def show_match_page(request):
    return render(request, 'v4_match/match_page.html')
