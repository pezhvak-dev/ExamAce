from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView
from hitcount.views import HitCountDetailView

from Weblog.models import Weblog


class AllWeblogs(ListView):
    model = Weblog
    context_object_name = 'weblogs'
    template_name = 'Weblog/weblog_list.html'

    def get_queryset(self):
        weblogs = Weblog.objects.select_related('category', 'author').order_by('-created_at')

        return weblogs


class WeblogDetail(HitCountDetailView, DetailView):
    model = Weblog
    context_object_name = 'weblog'
    template_name = 'Weblog/weblog_detail.html'
    count_hit = True

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        related_weblogs = self.object.get_related_weblogs(max_results=5)
        latest_weblogs = self.object.get_latest_weblogs()

        context['related_weblogs'] = related_weblogs
        context['latest_weblogs'] = latest_weblogs

        return context

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class WeblogsByCategory(ListView):
    model = Weblog
    context_object_name = 'weblogs'
    template_name = 'Weblog/weblogs_by_category.html'

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        weblogs = get_list_or_404(Weblog, category__slug=slug)

        return weblogs
