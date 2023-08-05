from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):
    header = CharFilter(lookup_expr='icontains', label='По заголовку')
    author__user__username = CharFilter(lookup_expr='icontains', label='По имени автора')
    time_in = DateFilter(field_name='time_in', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}), label='Позже чем')

    class Meta:
        model = Post
        fields = ['header', 'author__user__username', 'time_in']

    @property
    def qs(self):
        filter_posts = super().qs
        return filter_posts