from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Article

class ArticleListView(ListView):
    paginate_by = 10
    model = Article
    template_name = 'blog/article_list.html'
    ordering = ['-created_date']

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
