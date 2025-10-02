from .models import News, NewsCategory


def latest_news(request):
    latest_news = News.objects.all().order_by('-id')[:10]
    categories = NewsCategory.objects.all()

    context = {
        'latest_news': latest_news,
        'categories': categories,
    }

    return context