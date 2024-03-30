from django.views.generic import TemplateView

from Us.models import AboutUs


class About(TemplateView):
    template_name = "Us/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        about = AboutUs.objects.last()

        context['about'] = about

        return context
