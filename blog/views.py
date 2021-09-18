from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Article

class ArticleListView(ListView):
    paginate_by = 10
    model = Article
    template_name = 'blog/article_list.html'

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        object_list = self.model.objects.all().order_by('-created_date')
        if title:
            object_list = object_list.filter(title__icontains=title)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
