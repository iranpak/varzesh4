from django.shortcuts import render

# Create your views here.


def show_news_page(request):
    return render(request, 'v4_news/news_page.html')