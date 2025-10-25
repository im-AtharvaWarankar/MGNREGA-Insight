"""
MGNREGA API Views
-----------------
API endpoints for CivicView application.

Endpoints:
- /api/health/ - Health check
- /api/districts/ - District list/detail
- /api/districts/{id}/summary/ - Performance summary
- /api/districts/{id}/history/ - Historical performance
- /api/compare/ - District comparison

Following Reference.md format:
- Using AtomicViewSet for CRUD resources
- Using APIViews for custom actions
- Proper permissions, pagination, caching
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.cache import cache
from django.db.models import Avg, Q
from django.utils import timezone

from mgnrega.models import District, Performance, APIStatus
from mgnrega.serializers import (
    DistrictSerializer,
    DistrictListSerializer,
    PerformanceSerializer,
    PerformanceSummarySerializer,
    HistoricalPerformanceSerializer,
    ComparisonSerializer,
    APIStatusSerializer
)
from mgnrega.filters import DistrictFilter, PerformanceFilter
from atomicloops.viewsets import AtomicViewSet


class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring.
    
    Returns system status including database, redis, and last data fetch.
    Public endpoint (no authentication required).
    """
    
    authentication_classes = ()
    permission_classes = (AllowAny,)
    
    def get(self, request):
        """GET /api/health/"""
        
        # Check database connectivity
        try:
            District.objects.exists()
            db_status = True
        except Exception:
            db_status = False
        
        # Check Redis connectivity
        try:
            cache.set('health_check', 'ok', 10)
            cache.get('health_check')
            redis_status = True
        except Exception:
            redis_status = False
        
        # Get last data fetch status
        try:
            last_status = APIStatus.objects.filter(
                source='data.gov.in/mgnrega'
            ).order_by('-createdAt').first()
            
            if last_status:
                last_fetch_time = last_status.lastFetched
                last_fetch_status = last_status.status
            else:
                last_fetch_time = None
                last_fetch_status = 'never'
        except Exception:
            last_fetch_time = None
            last_fetch_status = 'error'
        
        # Overall status
        overall_status = 'ok' if (db_status and redis_status) else 'degraded'
        
        return Response({
            'status': overall_status,
            'timestamp': timezone.now().isoformat(),
            'database': db_status,
            'redis': redis_status,
            'lastFetch': last_fetch_time.isoformat() if last_fetch_time else None,
            'lastFetchStatus': last_fetch_status
        })


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for District model.
    
    Endpoints:
    - GET /api/districts/ - List all districts
    - GET /api/districts/{id}/ - District detail
    
    Public read-only access.
    """
    
    queryset = District.objects.all().order_by('state', 'name')
    permission_classes = [AllowAny]
    filterset_class = DistrictFilter
    search_fields = ('name', 'code', 'state')
    ordering_fields = ('name', 'state', 'population')
    ordering = ('state', 'name')
    
    def get_serializer_class(self):
        """Use lightweight serializer for lists"""
        if self.action == 'list':
            return DistrictListSerializer
        return DistrictSerializer
    
    @action(detail=True, methods=['get'], url_path='summary')
    def summary(self, request, pk=None):
        """
        GET /api/districts/{id}/summary/?year=YYYY&month=MM
        
        Returns current month performance summary with status indicators.
        """
        district = self.get_object()
        
        # Get year and month from query params (default to current)
        now = timezone.now()
        year = int(request.query_params.get('year', now.year))
        month = int(request.query_params.get('month', now.month))
        
        # Validate month
        if month < 1 or month > 12:
            return Response(
                {
                    'error': {
                        'code': 'INVALID_MONTH',
                        'message': 'Month must be between 1 and 12',
                        'details': {'month': month}
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check cache first
        cache_key = f'district:{pk}:summary:{year}-{month}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Get performance data
        try:
            performance = Performance.objects.select_related(
                'districtId'
            ).get(
                districtId=district,
                year=year,
                month=month
            )
        except Performance.DoesNotExist:
            return Response(
                {
                    'error': {
                        'code': 'NO_DATA_AVAILABLE',
                        'message': f'No performance data for {year}-{month:02d}',
                        'details': {
                            'district_id': pk,
                            'year': year,
                            'month': month
                        }
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serialize with status calculations
        serializer = PerformanceSummarySerializer(performance)
        data = serializer.data
        
        # Cache for 1 hour
        cache.set(cache_key, data, 3600)
        
        return Response(data)
    
    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        """
        GET /api/districts/{id}/history/?from=YYYY-MM&to=YYYY-MM
        
        Returns historical performance data (time series).
        """
        district = self.get_object()
        
        # Parse date range from query params
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        
        if not from_date or not to_date:
            return Response(
                {
                    'error': {
                        'code': 'INVALID_DATE_RANGE',
                        'message': 'Both from and to parameters required (format: YYYY-MM)',
                        'details': {
                            'from': from_date,
                            'to': to_date
                        }
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse YYYY-MM format
        try:
            from_year, from_month = map(int, from_date.split('-'))
            to_year, to_month = map(int, to_date.split('-'))
        except (ValueError, AttributeError):
            return Response(
                {
                    'error': {
                        'code': 'INVALID_DATE_FORMAT',
                        'message': 'Dates must be in YYYY-MM format',
                        'details': {
                            'from': from_date,
                            'to': to_date
                        }
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Build query for date range
        performances = Performance.objects.filter(
            districtId=district
        ).filter(
            Q(year__gt=from_year) | Q(year=from_year, month__gte=from_month)
        ).filter(
            Q(year__lt=to_year) | Q(year=to_year, month__lte=to_month)
        ).order_by('year', 'month')
        
        # Format data for time series
        data_points = []
        for perf in performances:
            data_points.append({
                'year': perf.year,
                'month': perf.month,
                'period': perf.period_display,
                'personDays': perf.personDays,
                'householdsWorked': perf.householdsWorked,
                'totalWages': float(perf.totalWages),
                'materialExpenditure': float(perf.materialExpenditure)
            })
        
        response_data = {
            'district': {
                'id': district.id,
                'name': district.name,
                'state': district.state
            },
            'period': {
                'from': from_date,
                'to': to_date
            },
            'data': data_points
        }
        
        return Response(response_data)


class ComparisonView(APIView):
    """
    District comparison endpoint.
    
    GET /api/compare/?districts=1,2,3&metric=person_days&period=YYYY-MM
    
    Compares multiple districts on a specific metric.
    Public endpoint.
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """GET /api/compare/"""
        
        # Parse query params
        district_ids = request.query_params.get('districts', '')
        metric = request.query_params.get('metric', 'personDays')
        period = request.query_params.get('period')
        
        # Validate inputs
        if not district_ids or not period:
            return Response(
                {
                    'error': {
                        'code': 'MISSING_PARAMETERS',
                        'message': 'Required parameters: districts, period',
                        'details': {
                            'districts': district_ids,
                            'period': period
                        }
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse district IDs
        try:
            district_ids = [int(id.strip()) for id in district_ids.split(',')]
        except ValueError:
            return Response(
                {
                    'error': {
                        'code': 'INVALID_DISTRICT_IDS',
                        'message': 'District IDs must be comma-separated numbers',
                        'details': {'districts': district_ids}
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse period (YYYY-MM)
        try:
            year, month = map(int, period.split('-'))
        except (ValueError, AttributeError):
            return Response(
                {
                    'error': {
                        'code': 'INVALID_PERIOD_FORMAT',
                        'message': 'Period must be in YYYY-MM format',
                        'details': {'period': period}
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate metric
        valid_metrics = {
            'person_days': 'personDays',
            'households_worked': 'householdsWorked',
            'total_wages': 'totalWages',
            'material_expenditure': 'materialExpenditure'
        }
        
        if metric not in valid_metrics:
            return Response(
                {
                    'error': {
                        'code': 'INVALID_METRIC',
                        'message': f'Metric must be one of: {", ".join(valid_metrics.keys())}',
                        'details': {'metric': metric}
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        field_name = valid_metrics[metric]
        
        # Fetch comparison data
        performances = Performance.objects.filter(
            districtId__in=district_ids,
            year=year,
            month=month
        ).select_related('districtId').order_by(f'-{field_name}')
        
        # Format results with ranking
        districts = []
        for rank, perf in enumerate(performances, 1):
            value = getattr(perf, field_name)
            districts.append({
                'id': perf.districtId.id,
                'name': perf.districtId.name,
                'state': perf.districtId.state,
                'value': float(value) if hasattr(value, '__float__') else value,
                'rank': rank
            })
        
        response_data = {
            'metric': metric,
            'period': {
                'year': year,
                'month': month,
                'display': f'{year}-{month:02d}'
            },
            'districts': districts
        }
        
        return Response(response_data)
