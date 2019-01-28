from django.shortcuts import render, get_object_or_404
from .models import News

# Create your views here.


def show_news_page(request, news_id):
    news = get_object_or_404(News, id = news_id)
    tags = news.tags.split('-')
    image = news.image.url[10:]
    print(news.image.url)
    return render(request, 'v4_news/news_page.html', {'news': news, 'tags': tags, 'image':image})