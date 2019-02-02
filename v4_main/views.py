from django.shortcuts import render
from v4_news.models import News

# Create your views here.


def show_main_page(request):
    last_news = News.objects.order_by('-created_at')[:10]
    return render(request, 'v4_main/homepage.html', {'last_news': last_news})

