"""
MGNREGA Admin Configuration
----------------------------
Admin interface for managing MGNREGA data.

Following prompt_rules.md ADMIN rules:
- Register all public models
- Provide list_display for key identifying fields
- Provide list_filter for high-cardinality enums and statuses
- Provide search_fields for frequently searched text fields
- Mark id, createdAt, updatedAt as readonly
- Default ordering by -createdAt
"""

from django.contrib import admin
from .models import District, Performance, APIStatus


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'state', 'population', 'createdAt')
    list_filter = ('state',)
    search_fields = ('name', 'code', 'state')
    readonly_fields = ('id', 'createdAt', 'updatedAt')
    ordering = ('state', 'name')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'state')
        }),
        ('Location Data', {
            'fields': ('population', 'lat', 'lon'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = (
        'districtId',
        'year',
        'month',
        'personDays',
        'householdsWorked',
        'totalWages',
        'createdAt'
    )
    list_filter = ('year', 'month', 'districtId__state')
    search_fields = (
        'districtId__name',
        'districtId__code'
    )
    readonly_fields = ('id', 'createdAt', 'updatedAt')
    ordering = ('-year', '-month', 'districtId__name')
    
    fieldsets = (
        (None, {
            'fields': ('districtId', 'year', 'month')
        }),
        ('Performance Metrics', {
            'fields': (
                'personDays',
                'householdsWorked',
                'totalWages',
                'materialExpenditure'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )


@admin.register(APIStatus)
class APIStatusAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'status',
        'lastFetched',
        'recordsProcessed',
        'recordsFailed',
        'success_rate_display',
        'createdAt'
    )
    list_filter = ('status', 'source')
    search_fields = ('source', 'message')
    readonly_fields = (
        'id',
        'createdAt',
        'success_rate_display'
    )
    ordering = ('-createdAt',)
    
    fieldsets = (
        (None, {
            'fields': ('source', 'status', 'lastFetched')
        }),
        ('Results', {
            'fields': (
                'recordsProcessed',
                'recordsFailed',
                'success_rate_display',
                'message'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'createdAt'),
            'classes': ('collapse',)
        }),
    )
    
    def success_rate_display(self, obj):
        """Display success rate as formatted percentage"""
        return f"{obj.success_rate:.2f}%"
    success_rate_display.short_description = 'Success Rate'
