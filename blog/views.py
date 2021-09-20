from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Tag

class ArticleListView(ListView):
    paginate_by = 10
    model = Article
    template_name = 'blog/article_list.html'

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        tag = self.request.GET.get('tag', '')
        object_list = self.model.objects.all().order_by('-created_date')
        tag_obj = get_object_or_404(Tag, title=tag) if tag else None
        if title and tag_obj:
            object_list = object_list.filter(title__icontains=title, tags=tag_obj)
        elif title:
            object_list = object_list.filter(title__icontains=title)
        elif tag_obj:
             object_list = object_list.filter(tags=tag_obj)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag', '')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
