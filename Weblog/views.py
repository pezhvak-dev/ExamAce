from django.contrib import messages
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, DetailView, View
from hitcount.views import HitCountDetailView

from Account.mixins import AuthenticatedUsersOnlyMixin
from Home.mixins import URLStorageMixin
from Weblog.models import Weblog, Comment


class AllWeblogs(URLStorageMixin, ListView):
    model = Weblog
    context_object_name = 'weblogs'
    template_name = 'Weblog/weblog_list.html'

    def get_queryset(self):
        weblogs = Weblog.objects.select_related('category', 'author').order_by('-created_at')

        return weblogs


class WeblogDetail(URLStorageMixin, HitCountDetailView, DetailView):
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


class WeblogsByCategory(URLStorageMixin, ListView):
    model = Weblog
    context_object_name = 'weblogs'
    template_name = 'Weblog/weblogs_by_category.html'

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        weblogs = get_list_or_404(Weblog, category__slug=slug)

        return weblogs


class AddComment(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        slug = kwargs.get('slug')

        weblog = get_object_or_404(Weblog, slug=slug)

        Comment.objects.create(user=user, text=text, weblog=weblog, parent_id=parent_id)
        messages.success(request, f"نظر شما با موفقیت ثبت شد.")

        return redirect(reverse("weblog:detail", kwargs={'slug': slug}))
