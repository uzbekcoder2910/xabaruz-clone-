from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import request
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from hitcount.views import HitCountDetailView

from .models import News, NewsCategory, Contact
from .forms import ContactForm, CommentForm
from config.custom_permissions import OnlyLoggedSuperUserMixin


# Create your views here.
class NewsListView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'news_list.html'


class NewsDetailView(HitCountDetailView, DetailView):
    model = News
    context_object_name = 'news_detail'
    template_name = 'news_detail.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        # news.view_count += 1
        # news.save()
        context['comments'] = news.comments.filter(active=True)
        context['comments_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = self.object
            comment.user = self.request.user
            comment.save()
            form = CommentForm()

        context = self.get_context_data()
        context['comments_form'] = form
        return self.render_to_response(context)


class NewsIndexView(ListView):
    model = News
    context_object_name = 'news_index_list'
    template_name = 'index.html'
    def get_queryset(self):
        return News.objects.order_by('-id')[:15]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        # Mahalliy Xabarlarni frontga yuborish uchun
        local_news = News.objects.all().filter(category__name='Mahalliy').order_by('-id')
        context['local_news'] = local_news[1:6]
        context['hot_news'] = local_news[0]
        # Xorijiy xabarlarni frontga yuborish uchun
        international_news = News.objects.all().filter(category__name='Xorij').order_by('-id')
        context['international_news'] = international_news[1:6]
        context['international_one'] = international_news[0]
        # Sport xabarlarni frontga yuborish uchun
        sport_news = News.objects.all().filter(category__name='Sport').order_by('-id')
        context['sport_news'] = sport_news[1:6]
        context['sport_one'] = sport_news[0]
        # Texnologiya xabarlarni frontga yuborish uchun
        tech_news = News.objects.all().filter(category__name='Texnologiya').order_by('-id')
        context['tech_news'] = tech_news[1:6]
        context['tech_one'] = tech_news[0]

        return context

class ContactPageView(FormView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('news_index_list')

    def form_valid(self, form):
        contact = form.save()
        print("✅ New contact submitted:")
        print("Name:", contact.name)
        print("Email:", contact.email)
        print("Message:", contact.message)
        return super().form_valid(form)

class Error404View(TemplateView):
    template_name = '404.html'

# class  SingleNewsListView(ListView):
#     model = News
#     context_object_name = 'news_list'
#     template_name = 'single_page.html'

class LocalNewsListView(ListView):
    model = News
    context_object_name = 'local_news_list'
    template_name = 'local.html'
    def get_queryset(self):
        news = News.objects.all().filter(category__name='Mahalliy').order_by('-id')
        return news

class InternationalNewsListView(ListView):
    model = News
    context_object_name = 'international_news_list'
    template_name = 'international.html'
    def get_queryset(self):
        news = News.objects.all().filter(category__name='Xorij').order_by('-id')
        return news

class TechNewsListView(ListView):
    model = News
    context_object_name = 'tech_news_list'
    template_name = 'technology.html'

    def get_queryset(self):
        news = News.objects.all().filter(category__name='Texnologiya').order_by('-id')
        return news

class SportNewsListView(ListView):
    model = News
    context_object_name = 'sport_news_list'
    template_name = 'sport.html'

    def get_queryset(self):
        news = News.objects.all().filter(category__name='Sport').order_by('-id')
        return news

class NewsUpdateView(OnlyLoggedSuperUserMixin, UpdateView):
    model = News
    fields = ['title', 'body', 'image', 'category', 'status',]
    template_name = 'crud/news_edit.html'
    success_url = reverse_lazy('news_index_list')



class NewsDeleteView(OnlyLoggedSuperUserMixin, DeleteView):
    model = News
    fields = '__all__'
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('news_index_list')


class NewsCreateView(OnlyLoggedSuperUserMixin, CreateView):
    model = News
    fields = '__all__'
    template_name = 'crud/news_create.html'


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users,
    }
    return render(request,'admin_page.html', context)

class SearchNewsListView(ListView):
    model = News
    context_object_name = 'all_news_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-id')