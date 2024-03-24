from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'Home/index.html'


class TempInfo(TemplateView):
    template_name = "Home/temp_info.html"
