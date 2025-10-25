"""
Celery tasks for MGNREGA data sync.

Tasks:
- fetch_mgnrega_data: Periodic task to fetch data from API
"""

from celery import shared_task
from celery.utils.log import get_task_logger
from utils.mgnrega_fetcher import MGNREGADataFetcher

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='default')
def fetch_mgnrega_data_task(self):
    """
    Celery task to fetch MGNREGA data from external API.
    
    Runs weekly via Celery Beat.
    Implements retry logic with exponential backoff.
    
    Returns:
        Dict with processing results
    """
    try:
        logger.info("Starting scheduled MGNREGA data fetch")
        
        fetcher = MGNREGADataFetcher()
        result = fetcher.fetch_and_sync()
        
        logger.info(
            f"Data fetch completed: {result['processed']} processed, "
            f"{result['failed']} failed"
        )
        
        return {
            'status': 'success',
            'processed': result['processed'],
            'failed': result['failed'],
        }
        
    except Exception as e:
        logger.error(f"Error in data fetch task: {e}", exc_info=True)
        
        # Retry with exponential backoff
        # Retry delays: 60s, 120s, 300s (5 min)
        retry_countdown = 60 * (2 ** self.request.retries)
        
        raise self.retry(
            exc=e,
            countdown=retry_countdown,
            max_retries=3
        )
