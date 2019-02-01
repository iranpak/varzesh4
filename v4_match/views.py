from django.shortcuts import render, get_object_or_404
from v4_match.models import *
# Create your views here.


def show_match_page(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    return render(request, 'v4_match/match_page.html', {'match': match})

