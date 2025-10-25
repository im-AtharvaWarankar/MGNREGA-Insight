"""
MGNREGA Data Fetcher Service
-----------------------------
Fetches and validates MGNREGA data from data.gov.in API.

This service:
- Connects to the external MGNREGA API
- Validates data schema and ranges
- Handles errors with retry logic
- Logs all operations for debugging
- Updates APIStatus for monitoring

Following prompt_rules.md and master prompt requirements.
"""

import requests
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from mgnrega.models import District, Performance, APIStatus

logger = logging.getLogger(__name__)


class MGNREGADataFetcher:
    """
    Fetches and processes MGNREGA district performance data.
    
    Implements robust error handling, validation, and retry logic.
    """
    
    # API configuration
    # NOTE: Update with actual API endpoint from data.gov.in
    API_BASE_URL = "https://www.data.gov.in/api/datastore/resource"
    API_RESOURCE_ID = "MGNREGA_RESOURCE_ID"  # To be updated
    API_KEY = None  # Set if required
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAYS = [60, 120, 300]  # Exponential backoff in seconds
    
    # Validation constants
    MIN_YEAR = 2006  # MGNREGA started in 2006
    VALID_MONTHS = range(1, 13)
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the fetcher.
        
        Args:
            api_key: Optional API key for data.gov.in
        """
        self.api_key = api_key or self.API_KEY
        self.session = requests.Session()
        self.api_status = None
        
    def fetch_and_sync(self) -> Dict:
        """
        Main method to fetch data and sync to database.
        
        Returns:
            Dict with status, counts, and messages
        """
        # Create APIStatus record
        self.api_status = APIStatus.objects.create(
            source='data.gov.in/mgnrega',
            status=APIStatus.StatusChoices.IN_PROGRESS,
            message='Starting data fetch...'
        )
        
        try:
            logger.info("Starting MGNREGA data fetch")
            
            # Fetch raw data from API
            raw_data = self._fetch_from_api()
            
            if not raw_data:
                return self._handle_failure(
                    "No data received from API"
                )
            
            # Process and validate data
            result = self._process_data(raw_data)
            
            # Update APIStatus with results
            self._update_status_success(result)
            
            logger.info(
                f"Data sync completed: {result['processed']} processed, "
                f"{result['failed']} failed"
            )
            
            return result
            
        except Exception as e:
            logger.exception(f"Fatal error during data fetch: {e}")
            return self._handle_failure(str(e))
    
    def _fetch_from_api(self) -> List[Dict]:
        """
        Fetch data from data.gov.in API with retry logic.
        
        Returns:
            List of raw data records
            
        Raises:
            Exception if all retries exhausted
        """
        url = f"{self.API_BASE_URL}/{self.API_RESOURCE_ID}"
        
        headers = {}
        if self.api_key:
            headers['api-key'] = self.api_key
        
        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(
                    f"Fetching data from API (attempt {attempt + 1}/"
                    f"{self.MAX_RETRIES})"
                )
                
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                
                data = response.json()
                records = data.get('records', [])
                
                logger.info(f"Received {len(records)} records from API")
                return records
                
            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"API request failed (attempt {attempt + 1}): {e}"
                )
                
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAYS[attempt]
                    logger.info(f"Retrying in {delay} seconds...")
                    import time
                    time.sleep(delay)
                else:
                    raise Exception(
                        f"API request failed after {self.MAX_RETRIES} "
                        f"attempts: {e}"
                    )
        
        return []
    
    def _process_data(self, raw_data: List[Dict]) -> Dict:
        """
        Process and validate raw data, then upsert to database.
        
        Args:
            raw_data: List of raw records from API
            
        Returns:
            Dict with processed/failed counts and error details
        """
        processed = 0
        failed = 0
        errors = []
        
        for record in raw_data:
            try:
                # Validate record
                is_valid, validation_errors = self._validate_record(record)
                
                if not is_valid:
                    failed += 1
                    errors.append({
                        'record': record,
                        'errors': validation_errors
                    })
                    logger.debug(
                        f"Invalid record: {validation_errors}"
                    )
                    continue
                
                # Transform and save
                self._upsert_performance(record)
                processed += 1
                
            except Exception as e:
                failed += 1
                errors.append({
                    'record': record,
                    'errors': [str(e)]
                })
                logger.error(
                    f"Error processing record: {e}",
                    exc_info=True
                )
        
        return {
            'processed': processed,
            'failed': failed,
            'errors': errors[:10]  # Keep first 10 errors for review
        }
    
    def _validate_record(
        self,
        record: Dict
    ) -> Tuple[bool, List[str]]:
        """
        Validate a single performance record.
        
        Args:
            record: Raw record dict
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        required_fields = [
            'district_code',
            'year',
            'month',
            'person_days',
            'households_worked',
            'total_wages'
        ]
        
        for field in required_fields:
            if field not in record or record[field] is None:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        # Validate year
        year = record.get('year')
        try:
            year = int(year)
            if year < self.MIN_YEAR:
                errors.append(
                    f"Invalid year {year} (must be >= {self.MIN_YEAR})"
                )
        except (ValueError, TypeError):
            errors.append(f"Invalid year format: {year}")
        
        # Validate month
        month = record.get('month')
        try:
            month = int(month)
            if month not in self.VALID_MONTHS:
                errors.append(
                    f"Invalid month {month} (must be 1-12)"
                )
        except (ValueError, TypeError):
            errors.append(f"Invalid month format: {month}")
        
        # Validate numeric fields are non-negative
        numeric_fields = [
            'person_days',
            'households_worked',
            'total_wages',
            'material_expenditure'
        ]
        
        for field in numeric_fields:
            value = record.get(field, 0)
            try:
                value = float(value)
                if value < 0:
                    errors.append(
                        f"{field} cannot be negative: {value}"
                    )
            except (ValueError, TypeError):
                errors.append(
                    f"Invalid {field} format: {value}"
                )
        
        # Validate district code exists
        district_code = record.get('district_code')
        if not District.objects.filter(code=district_code).exists():
            errors.append(
                f"District code {district_code} not found in database"
            )
        
        return len(errors) == 0, errors
    
    @transaction.atomic
    def _upsert_performance(self, record: Dict):
        """
        Insert or update performance record in database.
        
        Args:
            record: Validated record dict
        """
        district = District.objects.get(code=record['district_code'])
        
        year = int(record['year'])
        month = int(record['month'])
        
        # Get or create performance record
        performance, created = Performance.objects.update_or_create(
            districtId=district,
            year=year,
            month=month,
            defaults={
                'personDays': int(record.get('person_days', 0)),
                'householdsWorked': int(
                    record.get('households_worked', 0)
                ),
                'totalWages': Decimal(
                    str(record.get('total_wages', 0))
                ),
                'materialExpenditure': Decimal(
                    str(record.get('material_expenditure', 0))
                ),
            }
        )
        
        action = 'Created' if created else 'Updated'
        logger.debug(
            f"{action} performance record: "
            f"{district.name} {year}-{month:02d}"
        )
    
    def _update_status_success(self, result: Dict):
        """
        Update APIStatus with successful completion.
        
        Args:
            result: Processing result dict
        """
        self.api_status.status = (
            APIStatus.StatusChoices.SUCCESS
            if result['failed'] == 0
            else APIStatus.StatusChoices.PARTIAL
        )
        self.api_status.lastFetched = timezone.now()
        self.api_status.recordsProcessed = result['processed']
        self.api_status.recordsFailed = result['failed']
        
        if result['failed'] > 0:
            error_summary = '\n'.join([
                f"Record errors: {err['errors']}"
                for err in result['errors'][:5]
            ])
            self.api_status.message = (
                f"Partially completed. {result['failed']} records failed "
                f"validation.\n\nSample errors:\n{error_summary}"
            )
        else:
            self.api_status.message = (
                f"Successfully processed {result['processed']} records"
            )
        
        self.api_status.save()
    
    def _handle_failure(self, error_message: str) -> Dict:
        """
        Handle complete fetch failure.
        
        Args:
            error_message: Error description
            
        Returns:
            Failure result dict
        """
        self.api_status.status = APIStatus.StatusChoices.FAILURE
        self.api_status.message = error_message
        self.api_status.save()
        
        return {
            'processed': 0,
            'failed': 0,
            'errors': [],
            'status': 'failure',
            'message': error_message
        }


def create_sample_districts():
    """
    Helper function to create sample districts for testing.
    
    In production, districts should be seeded from official source.
    """
    sample_districts = [
        {
            'name': 'Ranchi',
            'code': 'JH-RAN',
            'state': 'Jharkhand',
            'population': 2914253
        },
        {
            'name': 'Dhanbad',
            'code': 'JH-DHN',
            'state': 'Jharkhand',
            'population': 2684487
        },
        {
            'name': 'Giridih',
            'code': 'JH-GIR',
            'state': 'Jharkhand',
            'population': 2445474
        },
        # Add more districts as needed
    ]
    
    for district_data in sample_districts:
        District.objects.get_or_create(
            code=district_data['code'],
            defaults=district_data
        )
    
    logger.info(
        f"Created/verified {len(sample_districts)} sample districts"
    )
