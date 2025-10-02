from django.contrib import admin
from .models import News, NewsCategory, Contact

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish_time', 'status')
    list_filter = ('status', 'publish_time', 'created_time')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['publish_time', 'status']

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email']

