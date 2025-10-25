"""
MGNREGA App Configuration
"""

from django.apps import AppConfig


class MgnregaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mgnrega'
    verbose_name = 'MGNREGA Performance Data'
