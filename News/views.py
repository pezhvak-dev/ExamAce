from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView
from hitcount.views import HitCountDetailView

from News.models import News


class AllNews(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'News/news_list.html'

    def get_queryset(self):
        news = News.objects.select_related('category', 'author').order_by('-created_at')

        return news


class NewsDetail(HitCountDetailView, DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'News/news_detail.html'
    count_hit = True

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        related_news = self.object.get_related_news(max_results=5)
        latest_news = self.object.get_latest_news()

        context['related_news'] = related_news
        context['latest_news'] = latest_news

        return context

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class NewsByCategory(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'News/news_by_category.html'

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        news = get_list_or_404(News, category__slug=slug)

        return news
