"""
Management command to fetch MGNREGA data manually.

Usage:
    python manage.py fetch_mgnrega_data
    python manage.py fetch_mgnrega_data --create-sample-districts
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from utils.mgnrega_fetcher import MGNREGADataFetcher, create_sample_districts


class Command(BaseCommand):
    help = 'Fetch MGNREGA performance data from data.gov.in API'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-sample-districts',
            action='store_true',
            help='Create sample districts before fetching data',
        )
        parser.add_argument(
            '--api-key',
            type=str,
            help='API key for data.gov.in (if required)',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*60
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'MGNREGA Data Fetch - CivicView'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                '='*60 + '\n'
            )
        )
        
        # Create sample districts if requested
        if options['create_sample_districts']:
            self.stdout.write('Creating sample districts...')
            try:
                create_sample_districts()
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ Sample districts created/verified\n'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error creating sample districts: {e}\n'
                    )
                )
                return
        
        # Initialize fetcher
        api_key = options.get('api_key')
        fetcher = MGNREGADataFetcher(api_key=api_key)
        
        self.stdout.write(
            f'Start time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
        self.stdout.write('Fetching data from data.gov.in API...\n')
        
        try:
            # Fetch and sync data
            result = fetcher.fetch_and_sync()
            
            # Display results
            self.stdout.write('\n' + '='*60)
            self.stdout.write('RESULTS')
            self.stdout.write('='*60)
            
            if result.get('status') == 'failure':
                self.stdout.write(
                    self.style.ERROR(
                        f'\n✗ Fetch failed: {result["message"]}\n'
                    )
                )
                return
            
            # Success or partial success
            processed = result['processed']
            failed = result['failed']
            total = processed + failed
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Total records: {total}'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Processed successfully: {processed}'
                )
            )
            
            if failed > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠ Failed validation: {failed}'
                    )
                )
                
                # Show sample errors
                if result.get('errors'):
                    self.stdout.write('\nSample validation errors:')
                    for i, error in enumerate(result['errors'][:5], 1):
                        self.stdout.write(
                            f"  {i}. {error['errors']}"
                        )
            
            self.stdout.write(
                f'\nEnd time: '
                f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}'
            )
            self.stdout.write('='*60 + '\n')
            
            if failed == 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ Data sync completed successfully!\n'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        '⚠ Data sync completed with some errors. '
                        'Check APIStatus model for details.\n'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'\n✗ Fatal error: {e}\n'
                )
            )
            raise
