#!/usr/bin/env python
"""
Script to create comprehensive sample data for MGNREGA Dashboard
- Creates districts for all major Indian states (5 districts per state, 19 states = 95 districts)
- Generates 36 months of performance data for each district
- Includes varied performance patterns (excellent, good, average, poor)
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.dev')
django.setup()

from mgnrega.models import District, Performance


def create_sample_data():
    """Create sample districts and performance data for major Indian states"""
    
    # Major Indian states with highest population - 8 states, 5 districts each = 40 districts
    districts_data = [
        # Uttar Pradesh (Population: 199.8 million) - India's most populous state
        {'name': 'Lucknow', 'code': 'UP-LKO-001', 'state': 'Uttar Pradesh', 'population': 4589838, 'lat': Decimal('26.8467'), 'lon': Decimal('80.9462')},
        {'name': 'Kanpur Nagar', 'code': 'UP-KNP-002', 'state': 'Uttar Pradesh', 'population': 4581006, 'lat': Decimal('26.4499'), 'lon': Decimal('80.3319')},
        {'name': 'Ghaziabad', 'code': 'UP-GZB-003', 'state': 'Uttar Pradesh', 'population': 4681645, 'lat': Decimal('28.6692'), 'lon': Decimal('77.4538')},
        {'name': 'Allahabad', 'code': 'UP-ALD-004', 'state': 'Uttar Pradesh', 'population': 5954391, 'lat': Decimal('25.4358'), 'lon': Decimal('81.8463')},
        {'name': 'Varanasi', 'code': 'UP-VNS-005', 'state': 'Uttar Pradesh', 'population': 3682194, 'lat': Decimal('25.3176'), 'lon': Decimal('82.9739')},
        
        # Maharashtra (Population: 112.4 million) - Most industrialized state
        {'name': 'Mumbai Suburban', 'code': 'MH-MUM-001', 'state': 'Maharashtra', 'population': 9356962, 'lat': Decimal('19.0760'), 'lon': Decimal('72.8777')},
        {'name': 'Pune', 'code': 'MH-PUN-002', 'state': 'Maharashtra', 'population': 9429408, 'lat': Decimal('18.5204'), 'lon': Decimal('73.8567')},
        {'name': 'Thane', 'code': 'MH-THN-003', 'state': 'Maharashtra', 'population': 11060148, 'lat': Decimal('19.2183'), 'lon': Decimal('72.9781')},
        {'name': 'Nagpur', 'code': 'MH-NAG-004', 'state': 'Maharashtra', 'population': 4653570, 'lat': Decimal('21.1458'), 'lon': Decimal('79.0882')},
        {'name': 'Nashik', 'code': 'MH-NSK-005', 'state': 'Maharashtra', 'population': 6109052, 'lat': Decimal('19.9975'), 'lon': Decimal('73.7898')},
        
        # Bihar (Population: 104.1 million) - High MGNREGA usage
        {'name': 'Patna', 'code': 'BR-PTN-001', 'state': 'Bihar', 'population': 5838465, 'lat': Decimal('25.5941'), 'lon': Decimal('85.1376')},
        {'name': 'East Champaran', 'code': 'BR-ECH-002', 'state': 'Bihar', 'population': 5099371, 'lat': Decimal('26.6467'), 'lon': Decimal('84.9120')},
        {'name': 'Muzaffarpur', 'code': 'BR-MZF-003', 'state': 'Bihar', 'population': 4801062, 'lat': Decimal('26.1225'), 'lon': Decimal('85.3906')},
        {'name': 'Madhubani', 'code': 'BR-MDB-004', 'state': 'Bihar', 'population': 4487379, 'lat': Decimal('26.3543'), 'lon': Decimal('86.0737')},
        {'name': 'Gaya', 'code': 'BR-GAY-005', 'state': 'Bihar', 'population': 4391418, 'lat': Decimal('24.7955'), 'lon': Decimal('85.0002')},
        
        # West Bengal (Population: 91.3 million)
        {'name': 'North 24 Parganas', 'code': 'WB-N24-001', 'state': 'West Bengal', 'population': 10009781, 'lat': Decimal('22.6157'), 'lon': Decimal('88.4005')},
        {'name': 'South 24 Parganas', 'code': 'WB-S24-002', 'state': 'West Bengal', 'population': 8161961, 'lat': Decimal('22.1629'), 'lon': Decimal('88.4348')},
        {'name': 'Barddhaman', 'code': 'WB-BRD-003', 'state': 'West Bengal', 'population': 7717563, 'lat': Decimal('23.2324'), 'lon': Decimal('87.8615')},
        {'name': 'Murshidabad', 'code': 'WB-MSD-004', 'state': 'West Bengal', 'population': 7103807, 'lat': Decimal('24.1751'), 'lon': Decimal('88.2426')},
        {'name': 'Kolkata', 'code': 'WB-KOL-005', 'state': 'West Bengal', 'population': 4496694, 'lat': Decimal('22.5726'), 'lon': Decimal('88.3639')},
        
        # Madhya Pradesh (Population: 72.6 million) - Central India
        {'name': 'Indore', 'code': 'MP-IDR-001', 'state': 'Madhya Pradesh', 'population': 3276697, 'lat': Decimal('22.7196'), 'lon': Decimal('75.8577')},
        {'name': 'Bhopal', 'code': 'MP-BPL-002', 'state': 'Madhya Pradesh', 'population': 2371061, 'lat': Decimal('23.2599'), 'lon': Decimal('77.4126')},
        {'name': 'Jabalpur', 'code': 'MP-JBP-003', 'state': 'Madhya Pradesh', 'population': 2463289, 'lat': Decimal('23.1815'), 'lon': Decimal('79.9864')},
        {'name': 'Gwalior', 'code': 'MP-GWL-004', 'state': 'Madhya Pradesh', 'population': 2032036, 'lat': Decimal('26.2183'), 'lon': Decimal('78.1828')},
        {'name': 'Dhar', 'code': 'MP-DHR-005', 'state': 'Madhya Pradesh', 'population': 2185793, 'lat': Decimal('22.5970'), 'lon': Decimal('75.2973')},
        
        # Rajasthan (Population: 68.5 million) - Largest state by area
        {'name': 'Jaipur', 'code': 'RJ-JPR-001', 'state': 'Rajasthan', 'population': 6626178, 'lat': Decimal('26.9124'), 'lon': Decimal('75.7873')},
        {'name': 'Jodhpur', 'code': 'RJ-JDH-002', 'state': 'Rajasthan', 'population': 3687165, 'lat': Decimal('26.2389'), 'lon': Decimal('73.0243')},
        {'name': 'Alwar', 'code': 'RJ-ALW-003', 'state': 'Rajasthan', 'population': 3674179, 'lat': Decimal('27.5530'), 'lon': Decimal('76.6346')},
        {'name': 'Nagaur', 'code': 'RJ-NGR-004', 'state': 'Rajasthan', 'population': 3307743, 'lat': Decimal('27.2023'), 'lon': Decimal('73.7340')},
        {'name': 'Udaipur', 'code': 'RJ-UDP-005', 'state': 'Rajasthan', 'population': 3068420, 'lat': Decimal('24.5854'), 'lon': Decimal('73.7125')},
        
        # Tamil Nadu (Population: 72.1 million) - South India powerhouse
        {'name': 'Chennai', 'code': 'TN-CHN-001', 'state': 'Tamil Nadu', 'population': 7088000, 'lat': Decimal('13.0827'), 'lon': Decimal('80.2707')},
        {'name': 'Coimbatore', 'code': 'TN-CBE-002', 'state': 'Tamil Nadu', 'population': 3458045, 'lat': Decimal('11.0168'), 'lon': Decimal('76.9558')},
        {'name': 'Tiruvallur', 'code': 'TN-TVL-003', 'state': 'Tamil Nadu', 'population': 3728104, 'lat': Decimal('13.1434'), 'lon': Decimal('79.9095')},
        {'name': 'Vellore', 'code': 'TN-VLR-004', 'state': 'Tamil Nadu', 'population': 3936331, 'lat': Decimal('12.9165'), 'lon': Decimal('79.1325')},
        {'name': 'Salem', 'code': 'TN-SLM-005', 'state': 'Tamil Nadu', 'population': 3482056, 'lat': Decimal('11.6643'), 'lon': Decimal('78.1460')},
        
        # Karnataka (Population: 61.1 million) - IT hub
        {'name': 'Bangalore Urban', 'code': 'KA-BLR-001', 'state': 'Karnataka', 'population': 9621551, 'lat': Decimal('12.9716'), 'lon': Decimal('77.5946')},
        {'name': 'Belgaum', 'code': 'KA-BLG-002', 'state': 'Karnataka', 'population': 4779661, 'lat': Decimal('15.8497'), 'lon': Decimal('74.4977')},
        {'name': 'Mysore', 'code': 'KA-MYS-003', 'state': 'Karnataka', 'population': 3001127, 'lat': Decimal('12.2958'), 'lon': Decimal('76.6394')},
        {'name': 'Tumkur', 'code': 'KA-TUM-004', 'state': 'Karnataka', 'population': 2678980, 'lat': Decimal('13.3379'), 'lon': Decimal('77.1006')},
        {'name': 'Gulbarga', 'code': 'KA-GLB-005', 'state': 'Karnataka', 'population': 2566326, 'lat': Decimal('17.3297'), 'lon': Decimal('76.8343')},
    ]
    
    print("="*80)
    print("🌏 Creating Comprehensive District Data for All Major Indian States")
    print("="*80)
    print(f"Creating {len(districts_data)} districts across 19 states...\n")
    
    # Create districts
    districts = []
    state_count = {}
    for data in districts_data:
        district, created = District.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"  ✅ Created: {district.name:25s} ({district.state})")
        else:
            print(f"  ℹ️  Exists: {district.name:25s} ({district.state})")
        districts.append(district)
        state_count[district.state] = state_count.get(district.state, 0) + 1
    
    print(f"\n📊 Summary: {len(districts)} districts across {len(state_count)} states")
    for state, count in sorted(state_count.items()):
        print(f"   {state:20s}: {count} districts")
    
    # Performance patterns for variety
    performance_patterns = {
        'excellent': {'base': 0.90, 'variance': 0.08},  # 90% ± 8%
        'good': {'base': 0.75, 'variance': 0.10},       # 75% ± 10%
        'average': {'base': 0.60, 'variance': 0.12},    # 60% ± 12%
        'poor': {'base': 0.45, 'variance': 0.10},       # 45% ± 10%
        'very_poor': {'base': 0.30, 'variance': 0.08},  # 30% ± 8%
    }
    
    # Assign performance patterns to states (for variety and realism)
    state_patterns = {
        'Andhra Pradesh': 'good',
        'Assam': 'average',
        'Bihar': 'poor',
        'Chhattisgarh': 'average',
        'Gujarat': 'excellent',
        'Haryana': 'good',
        'Jharkhand': 'poor',
        'Karnataka': 'excellent',
        'Kerala': 'excellent',
        'Madhya Pradesh': 'average',
        'Maharashtra': 'good',
        'Odisha': 'average',
        'Punjab': 'good',
        'Rajasthan': 'very_poor',
        'Tamil Nadu': 'excellent',
        'Telangana': 'good',
        'Uttar Pradesh': 'poor',
        'Uttarakhand': 'average',
        'West Bengal': 'average',
    }
    
    # Generate 36 months of data for each district
    print("\n"+"="*80)
    print("📅 Creating 36 Months of Performance Data")
    print("="*80)
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    total_created = 0
    for district in districts:
        pattern = performance_patterns[state_patterns.get(district.state, 'average')]
        base_performance = pattern['base']
        variance = pattern['variance']
        district_count = 0
        
        # Create 36 months of data
        for month_offset in range(36):
            month = current_month - month_offset
            year = current_year
            
            # Handle month/year rollover
            while month <= 0:
                month += 12
                year -= 1
            
            # Add seasonal variation (monsoon affects MGNREGA work)
            seasonal_factor = 1.0
            if month in [6, 7, 8, 9]:  # Monsoon months
                seasonal_factor = 0.92  # Slight dip during monsoon
            elif month in [10, 11, 12, 1]:  # Post-monsoon/winter
                seasonal_factor = 1.08  # Peak activity period
            
            # Add gradual improvement trend over time
            improvement_trend = 1 + (month_offset * 0.001)  # 0.1% improvement per month backwards
            
            # Calculate performance ratio with variations
            performance_ratio = base_performance * seasonal_factor / improvement_trend
            performance_ratio += random.uniform(-variance, variance)
            performance_ratio = max(0.15, min(0.98, performance_ratio))  # Clamp between 15% and 98%
            
            # Scale by population
            population_factor = district.population / 1000000  # Per million population
            
            # Generate realistic metrics
            personDays = int(random.randint(35000, 55000) * population_factor * performance_ratio)
            householdsWorked = int(random.randint(4000, 6000) * population_factor * performance_ratio)
            totalWages = Decimal(random.randint(17000000, 28000000)) * Decimal(population_factor) * Decimal(str(performance_ratio))
            materialExpenditure = Decimal(random.randint(8000000, 15000000)) * Decimal(population_factor) * Decimal(str(performance_ratio))
            
            performance, created = Performance.objects.get_or_create(
                districtId=district,
                year=year,
                month=month,
                defaults={
                    'personDays': personDays,
                    'householdsWorked': householdsWorked,
                    'totalWages': totalWages,
                    'materialExpenditure': materialExpenditure
                }
            )
            
            if created:
                district_count += 1
                total_created += 1
        
        print(f"  ✅ {district.name:25s} ({district.state:20s}): {district_count} months")
    
    print("\n"+"="*80)
    print("🎉 Sample Data Creation Complete!")
    print("="*80)
    print(f"   ✅ Created {len(districts)} districts across {len(state_count)} states")
    print(f"   ✅ Created {total_created} performance records (36 months × {len(districts)} districts)")
    print(f"   📅 Date range: {datetime(year, month, 1).strftime('%B %Y')} to {datetime(current_year, current_month, 1).strftime('%B %Y')}")
    print("\n📍 Next Steps:")
    print("   1. 🔧 Django Admin: http://localhost:8000/admin")
    print("      Login: admin@civicview.com / admin123")
    print("   2. 🌐 Frontend Dashboard: http://localhost:3001")
    print("   3. 🧪 Test with comprehensive multi-state data!")
    print("="*80)


if __name__ == '__main__':
    create_sample_data()
