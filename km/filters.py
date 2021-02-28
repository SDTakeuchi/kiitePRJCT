import django_filters
from django_filters import CharFilter, conf
from .models import *

def FILTERS_VERBOSE_LOOKUPS():
    from django_filters.conf import DEFAULTS

    verbose_lookups = DEFAULTS['VERBOSE_LOOKUPS'].copy()
    verbose_lookups.update({
        'icontains':'',
    })
    return verbose_lookups

class PostFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='質問タイトル')

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['date_created', 'date_updated','user', 'body']