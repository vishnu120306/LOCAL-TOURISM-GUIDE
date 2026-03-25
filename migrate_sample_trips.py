import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Itinerary

def migrate_trips():
    trips = [
        {
            'name': 'Golden Triangle of Kerala',
            'description': 'Explore the perfect blend of spice plantations, misty hills, and serene backwaters in this essential Kerala experience.',
            'duration': '5 Days / 4 Nights',
            'price': 15000.00,
        },
        {
            'name': 'Coastal Discovery',
            'description': 'Trace the stunning Malabar coast, visiting pristine beaches and historic light-houses for the ultimate sun-soaked escape.',
            'duration': '4 Days / 3 Nights',
            'price': 12000.00,
        },
        {
            'name': 'Mist & Mountains',
            'description': 'Ascend to the highest peaks of the Western Ghats for dramatic views and adventurous hiking trails.',
            'duration': '4 Days / 3 Nights',
            'price': 10000.00,
        },
        {
            'name': 'Cultural Heritage Trail',
            'description': 'Immerse yourself in the deep-rooted traditions of Kerala, from ancient temples to classical dance performances.',
            'duration': '3 Days / 2 Nights',
            'price': 8000.00,
        },
        {
            'name': 'Silent Valley Expedition',
            'description': 'Venture into the untouched rainforests of Kerala to spot rare species and experience the true "Silent Valley".',
            'duration': '2 Days / 1 Night',
            'price': 5000.00,
        },
        {
            'name': 'Munnar Mist & Tea',
            'description': 'Experience the beauty of Munnar tea gardens and the surrounding hills.',
            'duration': '3 Days / 2 Nights',
            'price': 7000.00,
        },
        {
            'name': 'Alleppey Backwater Bliss',
            'description': 'Relax on a houseboat and enjoy the serene backwaters of Alleppey.',
            'duration': '2 Days / 1 Night',
            'price': 6000.00,
        },
        {
            'name': 'Wild Wayanad Escape',
            'description': 'Discover the wildlife and natural beauty of Wayanad.',
            'duration': '3 Days / 2 Nights',
            'price': 9000.00,
        }
    ]

    for trip in trips:
        Itinerary.objects.update_or_create(name=trip['name'], defaults=trip)
    
    print(f"Successfully migrated {len(trips)} sample trips to the database.")

if __name__ == '__main__':
    migrate_trips()
