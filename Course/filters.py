import django_filters

from Course.models import Exam, Category


class ExamFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name='category', queryset=Category.objects.all())

    class Meta:
        model = Exam
        fields = {
            "price": ['lt', 'gt']
        }
