from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Article

class ArticleListView(ListView):
    paginate_by = 10
    model = Article
    template_name = 'blog/article_list.html'
    ordering = ['-created_date']

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        object_list = self.model.objects.all()
        if title:
            object_list = object_list.filter(title__icontains=title)
        return object_list

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
