from django_filters.rest_framework import FilterSet, CharFilter

from reviews.models import Title


class TitleFilterSet(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']
