import os
import django
import sys

# Add project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Category, Location

def seed_data():
    categories = [
        {'name': 'Attractions', 'icon': 'fas fa-landmark', 'description': 'Must-visit historical and modern landmarks.'},
        {'name': 'Events', 'icon': 'fas fa-calendar-alt', 'description': 'Cultural festivals and local happenings.'},
    ]

    for cat_data in categories:
        Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'icon': cat_data['icon'], 'description': cat_data['description']}
        )

    print("Seed data created successfully!")

if __name__ == '__main__':
    seed_data()
