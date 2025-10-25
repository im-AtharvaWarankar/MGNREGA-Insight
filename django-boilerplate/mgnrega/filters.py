"""
MGNREGA Filters
---------------
Filter classes for querying district and performance data.

Following prompt_rules.md FILTERS rules:
- Using appropriate filter base classes
- Custom filter fields for complex queries
- Proper lookup expressions
"""

import django_filters
from mgnrega.models import District, Performance


class DistrictFilter(django_filters.FilterSet):
    """
    Filter for District model.
    
    Supports filtering by:
    - state (exact match)
    - name (case-insensitive contains)
    - code (exact match)
    """
    
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    state = django_filters.CharFilter(
        field_name='state',
        lookup_expr='iexact'
    )
    code = django_filters.CharFilter(
        field_name='code',
        lookup_expr='iexact'
    )
    
    class Meta:
        model = District
        fields = ('state', 'name', 'code')


class PerformanceFilter(django_filters.FilterSet):
    """
    Filter for Performance model.
    
    Supports filtering by:
    - districtId (exact match)
    - state (via district relationship)
    - year (exact, gte, lte)
    - month (exact, gte, lte)
    - year_month (custom combined filter)
    """
    
    districtId = django_filters.NumberFilter(
        field_name='districtId'
    )
    state = django_filters.CharFilter(
        field_name='districtId__state',
        lookup_expr='iexact'
    )
    year = django_filters.NumberFilter(
        field_name='year'
    )
    year__gte = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='gte'
    )
    year__lte = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='lte'
    )
    month = django_filters.NumberFilter(
        field_name='month'
    )
    month__gte = django_filters.NumberFilter(
        field_name='month',
        lookup_expr='gte'
    )
    month__lte = django_filters.NumberFilter(
        field_name='month',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Performance
        fields = (
            'districtId',
            'state',
            'year',
            'month'
        )
