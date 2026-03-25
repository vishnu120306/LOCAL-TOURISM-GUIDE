import os
import django
import sys
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Guide, Booking, Location, Event, Transport, Category
from django.contrib.auth.models import User

def update_data():
    print("Starting data update...")

    # 1. Remove Demo Guide
    deleted_count, _ = Guide.objects.filter(name__icontains="Demo").delete()
    print(f"Deleted {deleted_count} guides with 'Demo' in the name.")
    
    # Also remove any guide named "John Doe" if it exists
    deleted_count, _ = Guide.objects.filter(name__icontains="John Doe").delete()
    print(f"Deleted {deleted_count} guides with 'John Doe' in the name.")

    # 2. Add Sample Trips (as Locations with a new Category)
    trip_category, created = Category.objects.get_or_create(
        name='Sample Trip',
        defaults={'icon': 'fas fa-route', 'description': 'Curated itineraries for your perfect vacation.'}
    )
    
    sample_trips = [
        {
            'name': 'Classical Kerala Tour (5 Days)',
            'description': 'Experience the best of Kerala with this 5-day itinerary covering Cochin, Munnar, and Alleppey. Includes heritage walks, tea garden visits, and a houseboat cruise.',
            'address': 'Cochin - Munnar - Alleppey',
            'image': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Backwaters & Beaches (4 Days)',
            'description': 'Relax and unwind with this water-themed trip. Spend 2 nights on a luxury houseboat in Alleppey and 2 nights at the pristine Varkala beach.',
            'address': 'Alleppey - Varkala',
            'image': 'https://images.unsplash.com/photo-1596627685289-4cb984577b21?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Wayanad Wilderness Trek (3 Days)',
            'description': 'For the adventure seekers. Trek through the dense forests of Wayanad, visit Edakkal Caves, and stay in a jungle resort.',
            'address': 'Wayanad, Kerala',
            'image': 'https://images.unsplash.com/photo-1445548677651-789f8992ad7c?auto=format&fit=crop&q=80&w=800'
        }
    ]

    for trip in sample_trips:
        image_url = trip.pop('image')
        loc, created = Location.objects.get_or_create(
            name=trip['name'],
            defaults={
                'category': trip_category,
                'description': trip['description'],
                'address': trip['address']
            }
        )
        if created:
            print(f"Created Sample Trip: {trip['name']}")
            # Ideally we would download the image here, but for now we'll rely on placeholders or manual update later if needed
            # Or we can reuse the download logic if we import it, but let's keep it simple.
            # We will just set a placeholder or let the template handle it.
            # actually better to try to set the image field if we can, but without downloading it's hard.
            # Let's just print it.
    
    # 3. Add Itineraries (Bookings) for User
    # Find user
    user = User.objects.filter(username__icontains='vishnu').first()
    if not user:
        user = User.objects.first()
        print(f"User 'vishnu' not found, using {user.username} instead.")
    else:
        print(f"Found user: {user.username}")

    if user:
        # Create Dummy Bookings
        
        # Booking 1: Houseboat
        transport = Transport.objects.filter(transport_type='BOAT').first()
        if transport:
            Booking.objects.get_or_create(
                user_name=user.username,
                user_email=user.email,
                transport=transport,
                date=datetime.now().date() + timedelta(days=5),
                defaults={'status': 'CONFIRMED'}
            )
            print(f"Booked Transport: {transport.name}")

        # Booking 2: Guide
        guide = Guide.objects.first()
        if guide:
            Booking.objects.get_or_create(
                user_name=user.username,
                user_email=user.email,
                guide=guide,
                date=datetime.now().date() + timedelta(days=6),
                defaults={'status': 'PENDING'}
            )
            print(f"Booked Guide: {guide.name}")

        # Booking 3: Event
        event = Event.objects.first()
        if event:
            Booking.objects.get_or_create(
                user_name=user.username,
                user_email=user.email,
                event=event,
                date=datetime.now().date() + timedelta(days=7),
                defaults={'status': 'CONFIRMED'}
            )
            print(f"Booked Event: {event.name}")

    print("Data update complete!")

if __name__ == '__main__':
    update_data()
