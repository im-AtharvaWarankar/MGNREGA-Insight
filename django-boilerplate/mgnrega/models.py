"""
MGNREGA Models
--------------
Models for storing MGNREGA district performance data.

Following prompt_rules.md:
- NO blank=True in any field (only null=True for database nullability)
- Using AutoField for primary keys (not UUID) for performance with large datasets
- All field names follow project conventions (camelCase)
- Proper indexing for query performance
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class District(models.Model):
    """
    Represents a district participating in MGNREGA program.
    
    Indexed fields: name, code (unique), state for fast lookups.
    Geolocation fields (lat/lon) support future map-based features.
    """
    id = models.AutoField(
        verbose_name=_('Id'),
        primary_key=True,
        db_column='id'
    )
    createdAt = models.DateTimeField(
        verbose_name=_('Create Date'),
        auto_now_add=True,
        db_column='created_at'
    )
    updatedAt = models.DateTimeField(
        verbose_name=_('Update Date'),
        auto_now=True,
        db_column='updated_at'
    )
    name = models.CharField(
        verbose_name=_('District Name'),
        max_length=255,
        db_column='name',
        db_index=True,
        help_text="Official district name"
    )
    code = models.CharField(
        verbose_name=_('District Code'),
        max_length=50,
        unique=True,
        db_column='code',
        help_text="Official district code from MGNREGA system"
    )
    state = models.CharField(
        verbose_name=_('State'),
        max_length=100,
        db_column='state',
        db_index=True,
        help_text="Indian state name"
    )
    population = models.BigIntegerField(
        verbose_name=_('Population'),
        null=True,
        db_column='population',
        validators=[MinValueValidator(0)],
        help_text="District population for per-capita calculations"
    )
    lat = models.DecimalField(
        verbose_name=_('Latitude'),
        max_digits=10,
        decimal_places=7,
        null=True,
        db_column='lat',
        validators=[MinValueValidator(Decimal('-90')), MaxValueValidator(Decimal('90'))],
        help_text="Latitude for geolocation mapping"
    )
    lon = models.DecimalField(
        verbose_name=_('Longitude'),
        max_digits=10,
        decimal_places=7,
        null=True,
        db_column='lon',
        validators=[MinValueValidator(Decimal('-180')), MaxValueValidator(Decimal('180'))],
        help_text="Longitude for geolocation mapping"
    )

    class Meta:
        db_table = 'district'
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        ordering = ['state', 'name']
        managed = True
        indexes = [
            models.Index(fields=['state', 'name'], name='idx_state_name'),
        ]

    def __str__(self):
        return f"{self.name}, {self.state}"


class Performance(models.Model):
    """
    Monthly performance metrics for a district.
    
    Composite unique constraint on (district, year, month) ensures one record per district-month.
    Indexed on (district, year, month) for time-series queries.
    """
    id = models.AutoField(
        verbose_name=_('Id'),
        primary_key=True,
        db_column='id'
    )
    createdAt = models.DateTimeField(
        verbose_name=_('Create Date'),
        auto_now_add=True,
        db_column='created_at'
    )
    updatedAt = models.DateTimeField(
        verbose_name=_('Update Date'),
        auto_now=True,
        db_column='updated_at'
    )
    districtId = models.ForeignKey(
        District,
        verbose_name=_('District'),
        related_name='performances',
        db_column='district_id',
        on_delete=models.CASCADE,
        help_text="District for this performance record"
    )
    year = models.IntegerField(
        verbose_name=_('Year'),
        db_column='year',
        db_index=True,
        validators=[MinValueValidator(2006)],  # MGNREGA started in 2006
        help_text="Year (YYYY format, >= 2006)"
    )
    month = models.IntegerField(
        verbose_name=_('Month'),
        db_column='month',
        db_index=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Month (1-12)"
    )
    personDays = models.BigIntegerField(
        verbose_name=_('Person Days'),
        default=0,
        db_column='person_days',
        validators=[MinValueValidator(0)],
        help_text="Total person-days of employment generated"
    )
    householdsWorked = models.BigIntegerField(
        verbose_name=_('Households Worked'),
        default=0,
        db_column='households_worked',
        validators=[MinValueValidator(0)],
        help_text="Number of households provided employment"
    )
    totalWages = models.DecimalField(
        verbose_name=_('Total Wages'),
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        db_column='total_wages',
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total wages paid (in INR)"
    )
    materialExpenditure = models.DecimalField(
        verbose_name=_('Material Expenditure'),
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        db_column='material_expenditure',
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total material expenditure (in INR)"
    )

    class Meta:
        db_table = 'performance'
        verbose_name = _('Performance')
        verbose_name_plural = _('Performance Records')
        ordering = ['-year', '-month']
        managed = True
        unique_together = [('districtId', 'year', 'month')]
        indexes = [
            models.Index(fields=['districtId', 'year', 'month'], name='idx_district_period'),
            models.Index(fields=['year', 'month'], name='idx_period'),
        ]

    def __str__(self):
        return f"{self.districtId.name} - {self.year}-{self.month:02d}"

    @property
    def period_display(self):
        """Return formatted period string: YYYY-MM"""
        return f"{self.year}-{self.month:02d}"


class APIStatus(models.Model):
    """
    Tracks external API fetch operations.
    
    Used for monitoring, debugging, and fallback logic.
    Records details of each data sync attempt.
    """
    
    class StatusChoices(models.TextChoices):
        SUCCESS = 'success', _('Success')
        FAILURE = 'failure', _('Failure')
        PARTIAL = 'partial', _('Partial')
        IN_PROGRESS = 'in_progress', _('In Progress')

    id = models.AutoField(
        verbose_name=_('Id'),
        primary_key=True,
        db_column='id'
    )
    createdAt = models.DateTimeField(
        verbose_name=_('Create Date'),
        auto_now_add=True,
        db_column='created_at'
    )
    updatedAt = models.DateTimeField(
        verbose_name=_('Update Date'),
        auto_now=True,
        db_column='updated_at'
    )
    source = models.CharField(
        verbose_name=_('Source'),
        max_length=100,
        db_column='source',
        help_text="API source identifier (e.g., 'data.gov.in/mgnrega')"
    )
    lastFetched = models.DateTimeField(
        verbose_name=_('Last Fetched'),
        null=True,
        db_column='last_fetched',
        help_text="Timestamp of last successful fetch"
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGRESS,
        db_column='status',
        help_text="Status of the fetch operation"
    )
    message = models.TextField(
        verbose_name=_('Message'),
        null=True,
        db_column='message',
        help_text="Error details or summary message"
    )
    recordsProcessed = models.IntegerField(
        verbose_name=_('Records Processed'),
        default=0,
        db_column='records_processed',
        validators=[MinValueValidator(0)],
        help_text="Number of records successfully processed"
    )
    recordsFailed = models.IntegerField(
        verbose_name=_('Records Failed'),
        default=0,
        db_column='records_failed',
        validators=[MinValueValidator(0)],
        help_text="Number of records that failed validation"
    )
    createdAt = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
        db_column='created_at'
    )

    class Meta:
        db_table = 'api_status'
        verbose_name = _('API Status')
        verbose_name_plural = _('API Statuses')
        ordering = ['-createdAt']
        managed = True

    def __str__(self):
        return f"{self.source} - {self.status} - {self.createdAt}"

    @property
    def success_rate(self):
        """Calculate success rate as percentage"""
        total = self.recordsProcessed + self.recordsFailed
        if total == 0:
            return 0.0
        return (self.recordsProcessed / total) * 100
