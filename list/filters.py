import django_filters
from django.db.models import Q

from .models import *


class PerFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Поиск по адресу или кад.номеру")
    year_per = django_filters.ModelChoiceFilter(queryset=Year.objects.all().order_by('-id'), empty_label=None )
    oks__tip_oks = django_filters.ModelChoiceFilter(label="Тип объекта", queryset=Tip.objects.all(), empty_label='Тип не выбран')

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(oks__cad_num__icontains=value) | Q(oks__adr_oks__icontains=value)
        )

    class Meta:
        model = Per
        fields = {
            'year_per',
            #'cad_num',
            'oks__tip_oks',
            #'adr_oks',
            #'q',

        }


class OksFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Поиск по адресу или кад.номеру")
    per__year_per = django_filters.ModelChoiceFilter(label="Год перечня", queryset=Year.objects.all().order_by('-id'),
                                                     empty_label=None, exclude=True)
    tip_oks = django_filters.ModelChoiceFilter(label="Тип объекта", queryset=Tip.objects.all(),
                                               empty_label='Тип не выбран')

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(cad_num__icontains=value) | Q(adr_oks__icontains=value)
        )

    class Meta:
        model = Oks
        fields = {
            'per__year_per',
            #'cad_num',
            'tip_oks',
            #'adr_oks',
            #'q',

        }