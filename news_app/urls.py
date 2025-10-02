from django.urls import path
from .views import NewsListView, NewsDetailView, NewsIndexView, ContactPageView, Error404View, \
    LocalNewsListView, InternationalNewsListView, TechNewsListView, SportNewsListView


urlpatterns = [
    path('', NewsIndexView.as_view(), name='news_index_list'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('news/error404/', Error404View.as_view(), name='error404'),
    # path('news/<int:pk>/', SingleNewsListView.as_view(), name='news_index'),
    path('local/', LocalNewsListView.as_view(), name='local_news_list'),
    path('foreign/', InternationalNewsListView.as_view(), name='foreign_news_list'),
    path('technology/', TechNewsListView.as_view(), name='tech_news_list'),
    path('sport/', SportNewsListView.as_view(), name='sport_news_list'),
]