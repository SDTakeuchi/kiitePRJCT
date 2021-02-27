import django_filters
from django_filters import CharFilter
from .models import *

class PostFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='質問タイトル')

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['date_created', 'date_updated','user', 'body']