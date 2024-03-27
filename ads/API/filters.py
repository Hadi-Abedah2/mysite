from ads.models import Ad
import django_filters


class AdFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains')
    price_gte = django_filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_lte = django_filters.NumberFilter(lookup_expr='lte', field_name='price')
    tags = django_filters.CharFilter(lookup_expr='icontains', field_name='tags__name')

    class Meta:
        model = Ad
        fields = ['title', 'price_gte', 'price_lte']


