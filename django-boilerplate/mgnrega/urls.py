"""
MGNREGA URL Configuration
--------------------------
URL routing for CivicView MGNREGA API endpoints.

Following prompt_rules.md URL rules:
- Using DefaultRouter for ViewSets
- Kebab-case for URL paths
- Clear, RESTful structure
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from mgnrega.views import (
    HealthCheckView,
    DistrictViewSet,
    ComparisonView
)

# Router for ViewSets
router = DefaultRouter()
router.register('districts', DistrictViewSet, basename='district')

# URL patterns
urlpatterns = [
    # Health check endpoint
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Comparison endpoint
    path('compare/', ComparisonView.as_view(), name='district-compare'),
]

# Add router URLs
urlpatterns += router.urls
