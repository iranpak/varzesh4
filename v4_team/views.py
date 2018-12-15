from django.shortcuts import render

# Create your views here.


def show_team(request):
    return render(request, 'v4_team/team_page.html')
