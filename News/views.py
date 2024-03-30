from django.shortcuts import render, get_object_or_404
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView

from News.models import News


class AllNews(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'News/news_list.html'

    def get_queryset(self):
        news = News.objects.select_related('category', 'author').order_by('-created_at')

        return news


class NewDetail(DetailView):
    model = News
    context_object_name = 'new'
    template_name = 'News/new_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'author')

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})