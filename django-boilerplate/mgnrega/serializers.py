"""
MGNREGA Serializers
-------------------
Serializers for District and Performance models.

Following Reference.md format:
- Using AtomicSerializer base where appropriate
- Proper field definitions with SerializerMethodField
- get_fields and list_fields in Meta class
"""

from rest_framework import serializers
from django.db.models import Avg
from mgnrega.models import District, Performance, APIStatus
from atomicloops.serializers import AtomicSerializer


class DistrictSerializer(serializers.ModelSerializer):
    """
    Serializer for District model.
    Used for list and detail endpoints.
    """
    
    class Meta:
        model = District
        fields = (
            'id',
            'name',
            'code',
            'state',
            'population',
            'lat',
            'lon',
            'createdAt',
            'updatedAt'
        )
        get_fields = fields
        list_fields = (
            'id',
            'name',
            'code',
            'state',
            'population'
        )
        read_only_fields = ('id', 'createdAt', 'updatedAt')


class DistrictListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for district listings.
    Excludes geolocation data for faster responses.
    """
    
    class Meta:
        model = District
        fields = (
            'id',
            'name',
            'code',
            'state',
            'population'
        )


class PerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Performance model.
    Includes district details and computed status fields.
    """
    
    districtName = serializers.CharField(
        source='districtId.name',
        read_only=True
    )
    districtCode = serializers.CharField(
        source='districtId.code',
        read_only=True
    )
    state = serializers.CharField(
        source='districtId.state',
        read_only=True
    )
    periodDisplay = serializers.CharField(
        source='period_display',
        read_only=True
    )
    
    class Meta:
        model = Performance
        fields = (
            'id',
            'districtId',
            'districtName',
            'districtCode',
            'state',
            'year',
            'month',
            'periodDisplay',
            'personDays',
            'householdsWorked',
            'totalWages',
            'materialExpenditure',
            'createdAt',
            'updatedAt'
        )
        get_fields = fields
        list_fields = (
            'id',
            'districtId',
            'districtName',
            'districtCode',
            'state',
            'year',
            'month',
            'periodDisplay',
            'personDays',
            'householdsWorked',
            'totalWages',
            'materialExpenditure'
        )
        read_only_fields = ('id', 'createdAt', 'updatedAt')


class PerformanceSummarySerializer(serializers.Serializer):
    """
    Serializer for district performance summary with status indicators.
    
    Calculates color-coded status based on state averages:
    - Good (green): >= 80% of state average
    - Average (amber): 50-79% of state average
    - Poor (red): < 50% of state average
    """
    
    district = DistrictListSerializer(read_only=True)
    period = serializers.DictField(read_only=True)
    metrics = serializers.DictField(read_only=True)
    status = serializers.DictField(read_only=True)
    comparisonToPreviousMonth = serializers.DictField(
        read_only=True,
        required=False
    )
    
    def to_representation(self, instance):
        """
        Custom representation with computed status fields.
        
        instance should be a Performance object
        """
        # Get state average for the same period
        state_avg = Performance.objects.filter(
            districtId__state=instance.districtId.state,
            year=instance.year,
            month=instance.month
        ).aggregate(
            avg_person_days=Avg('personDays'),
            avg_households=Avg('householdsWorked'),
            avg_wages=Avg('totalWages')
        )
        
        # Calculate status for each metric
        def calculate_status(value, avg_value):
            """Calculate status based on percentage of average"""
            if avg_value == 0 or avg_value is None:
                return 'neutral'
            
            # Convert to float to handle Decimal types
            percentage = (float(value) / float(avg_value)) * 100
            
            if percentage >= 80:
                return 'good'
            elif percentage >= 50:
                return 'average'
            else:
                return 'poor'
        
        # Get previous month data for comparison
        prev_month = instance.month - 1 if instance.month > 1 else 12
        prev_year = instance.year if instance.month > 1 else instance.year - 1
        
        try:
            prev_performance = Performance.objects.get(
                districtId=instance.districtId,
                year=prev_year,
                month=prev_month
            )
            
            # Calculate percentage changes
            def calc_change(current, previous):
                if previous == 0:
                    return 0
                return ((current - previous) / previous) * 100
            
            comparison = {
                'personDaysChange': calc_change(
                    instance.personDays,
                    prev_performance.personDays
                ),
                'householdsChange': calc_change(
                    instance.householdsWorked,
                    prev_performance.householdsWorked
                ),
                'wagesChange': calc_change(
                    float(instance.totalWages),
                    float(prev_performance.totalWages)
                )
            }
        except Performance.DoesNotExist:
            comparison = None
        
        return {
            'district': {
                'id': instance.districtId.id,
                'name': instance.districtId.name,
                'state': instance.districtId.state,
                'code': instance.districtId.code
            },
            'period': {
                'year': instance.year,
                'month': instance.month,
                'display': instance.period_display
            },
            'metrics': {
                'personDays': instance.personDays,
                'householdsWorked': instance.householdsWorked,
                'totalWages': float(instance.totalWages),
                'materialExpenditure': float(instance.materialExpenditure)
            },
            'status': {
                'personDaysStatus': calculate_status(
                    instance.personDays,
                    state_avg['avg_person_days']
                ),
                'householdsStatus': calculate_status(
                    instance.householdsWorked,
                    state_avg['avg_households']
                ),
                'wagesStatus': calculate_status(
                    float(instance.totalWages),
                    state_avg['avg_wages']
                )
            },
            'comparisonToPreviousMonth': comparison
        }


class HistoricalPerformanceSerializer(serializers.Serializer):
    """
    Serializer for historical performance data (time series).
    """
    
    district = DistrictListSerializer(read_only=True)
    period = serializers.DictField(read_only=True)
    data = serializers.ListField(read_only=True)


class ComparisonSerializer(serializers.Serializer):
    """
    Serializer for district comparison data.
    """
    
    metric = serializers.CharField(read_only=True)
    period = serializers.DictField(read_only=True)
    districts = serializers.ListField(read_only=True)


class APIStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for API Status model.
    Used in health check endpoint.
    """
    
    successRate = serializers.SerializerMethodField()
    
    class Meta:
        model = APIStatus
        fields = (
            'id',
            'source',
            'lastFetched',
            'status',
            'message',
            'recordsProcessed',
            'recordsFailed',
            'successRate',
            'createdAt'
        )
        read_only_fields = fields
    
    def get_successRate(self, obj):
        """Return formatted success rate"""
        return f"{obj.success_rate:.2f}%"
