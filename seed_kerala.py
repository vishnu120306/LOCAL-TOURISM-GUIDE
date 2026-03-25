import os
import django
import sys
from datetime import datetime, timedelta
import urllib.request
from django.core.files.base import ContentFile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Category, Location, Event, Guide, Transport

def download_image(url):
    try:
        # User-Agent header is often required by servers to allow scraping/downloading
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return ContentFile(response.read())
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
    return None

def seed_kerala_data():
    # Categories
    attractions_cat, _ = Category.objects.get_or_create(
        name='Attractions', 
        defaults={'icon': 'fas fa-landmark', 'description': 'Must-visit spots in Kerala.'}
    )
    events_cat, _ = Category.objects.get_or_create(
        name='Events', 
        defaults={'icon': 'fas fa-calendar-alt', 'description': 'Traditional and modern festivals.'}
    )

    # ATTRACTIONS - With Images
    attractions = [
        {
            'name': 'Munnar Tea Gardens',
            'category': attractions_cat,
            'description': 'Lush green tea plantations with rolling hills and cool climate. A paradise for nature lovers.',
            'address': 'Idukki District, Kerala',
            'latitude': 10.0889,
            'longitude': 77.0595,
            'image': 'https://images.unsplash.com/photo-1593693397690-362ae9666ec2?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Alleppey Backwaters',
            'category': attractions_cat,
            'description': 'Famous for its houseboat cruises and scenic waterway networks. Experience the Venice of the East.',
            'address': 'Alappuzha, Kerala',
            'latitude': 9.4981,
            'longitude': 76.3388,
            'image': 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/30/fa/77/05/alleppey-backwaters-vibe.jpg?w=1200&h=-1&s=1'
        },
        {
            'name': 'Fort Kochi',
            'category': attractions_cat,
            'description': 'A historic area known for its colonial charm, Chinese fishing nets, and vibrant art scene.',
            'address': 'Ernakulam, Kerala',
            'latitude': 9.9658,
            'longitude': 76.2421,
            'image': 'https://images.unsplash.com/photo-1589187151003-073a7682a8ca?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Wayanad Wildlife Sanctuary',
            'category': attractions_cat,
            'description': 'Home to diverse wildlife including elephants and tigers. Perfect for trekking and safari.',
            'address': 'Wayanad, Kerala',
            'latitude': 11.6854,
            'longitude': 76.1320,
            'image': 'https://images.unsplash.com/photo-1627311026002-311956f147cc?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Periyar National Park',
            'category': attractions_cat,
            'description': 'One of the finest wildlife reserves in India, known for its tiger and elephant populations.',
            'address': 'Thekkady, Kerala',
            'latitude': 9.6031,
            'longitude': 77.1616,
            'image': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Kovalam Beach',
            'category': attractions_cat,
            'description': 'Famous crescent-shaped beach with lighthouse views. Popular for swimming and sunbathing.',
            'address': 'Thiruvananthapuram, Kerala',
            'latitude': 8.3988,
            'longitude': 76.9782,
            'image': 'https://images.unsplash.com/photo-1590050752117-238cb0fb88b6?auto=format&fit=crop&q=80&w=800'
        },
    ]

    for a in attractions:
        image_url = a.pop('image', None)
        obj, created = Location.objects.update_or_create(name=a['name'], defaults=a)
        if image_url and (created or not obj.image):
            print(f"Downloading image for {a['name']}...")
            img_content = download_image(image_url)
            if img_content:
                obj.image.save(f"{a['name'].replace(' ', '_').lower()}.jpg", img_content, save=True)
                print(f"Saved image for {a['name']}")

    # CULTURAL EVENTS - With Images
    events = [
        {
            'name': 'Thrissur Pooram',
            'description': 'The most colorful and spectacular temple festival of Kerala featuring decorated elephants.',
            'location_name': 'Fort Kochi', # Using name to look up
            'start_date': datetime.now() + timedelta(days=60),
            'end_date': datetime.now() + timedelta(days=62),
            'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Thrissur_Pooram_-_Kudamattam.jpg/1200px-Thrissur_Pooram_-_Kudamattam.jpg'
        },
        {
            'name': 'Nehru Trophy Boat Race',
            'description': 'The famous snake boat race held annually on the Punnamada Lake in Alleppey.',
            'location_name': 'Alleppey Backwaters',
            'start_date': datetime.now() + timedelta(days=30),
            'end_date': datetime.now() + timedelta(days=31),
            'image': 'https://images.unsplash.com/photo-1567157577861-53625f2066d7?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Onam Festival',
            'description': 'Kerala\'s harvest festival celebrating King Mahabali with elaborate feasts and Vallam Kali.',
            'location_name': 'Fort Kochi',
            'start_date': datetime.now() + timedelta(days=90),
            'end_date': datetime.now() + timedelta(days=100),
            'image': 'https://images.unsplash.com/photo-1603957814864-4e78b1d6f467?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Theyyam Performance',
            'description': 'Ancient ritualistic art form of North Kerala with vibrant costumes and divine possession.',
            'location_name': 'Wayanad Wildlife Sanctuary',
            'start_date': datetime.now() + timedelta(days=45),
            'end_date': datetime.now() + timedelta(days=46),
            'image': 'https://images.unsplash.com/photo-1614088484180-2d854045f4d3?auto=format&fit=crop&q=80&w=800'
        },
        {
            'name': 'Cochin Carnival',
            'description': 'New Year celebration in Fort Kochi with parades, music, and the burning of Pappanji.',
            'location_name': 'Fort Kochi',
            'start_date': datetime.now() + timedelta(days=120),
            'end_date': datetime.now() + timedelta(days=121),
            'image': 'https://images.unsplash.com/photo-1514525253440-b39b56360c49?auto=format&fit=crop&q=80&w=800'
        },
    ]

    for e in events:
        image_url = e.pop('image', None)
        loc_name = e.pop('location_name')
        location = Location.objects.filter(name=loc_name).first()
        
        if location:
            e['location'] = location
            obj, created = Event.objects.update_or_create(name=e['name'], defaults=e)
            # Force update for Thrissur Pooram or if image is missing
            if image_url and (created or not obj.image or e['name'] == 'Thrissur Pooram'):
                print(f"Downloading image for {e['name']}...")
                img_content = download_image(image_url)
                if img_content:
                    obj.image.save(f"{e['name'].replace(' ', '_').lower()}.jpg", img_content, save=True)
                    print(f"Saved image for {e['name']}")


    # LOCAL TRANSPORT - With Images
    transports = [
        {'name': 'Kerala Houseboat', 'transport_type': 'BOAT', 'description': 'Luxurious overnight stay on traditional Kettuvallam boats through the backwaters.', 'price_per_km': 1500, 'image': 'https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&q=80&w=800'},
        {'name': 'Shikara Boat', 'transport_type': 'BOAT', 'description': 'Small traditional boats for short backwater rides perfect for photography.', 'price_per_km': 500, 'image': 'https://images.unsplash.com/photo-1597825006733-4f9a56593466?auto=format&fit=crop&q=80&w=800'},
        {'name': 'Kochi Tourist Cab', 'transport_type': 'TAXI', 'description': 'Comfortable AC sedan for long-distance travel across Kerala.', 'price_per_km': 18, 'image': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&q=80&w=800'},
        {'name': 'Innova Crysta', 'transport_type': 'TAXI', 'description': 'Premium SUV for family trips and group tours across hill stations.', 'price_per_km': 25, 'image': 'https://images.unsplash.com/photo-1550478051-4e47a96020c0?auto=format&fit=crop&q=80&w=800'},
        {'name': 'Auto Rickshaw', 'transport_type': 'TUKTUK', 'description': 'Iconic three-wheeler for short city trips and local exploration.', 'price_per_km': 12, 'image': 'https://images.unsplash.com/photo-1584950746656-3c22b9f390d4?auto=format&fit=crop&q=80&w=800'},
        {'name': 'KSRTC Tourist Bus', 'transport_type': 'BUS', 'description': 'Government-operated tourist buses connecting major destinations.', 'price_per_km': 5, 'image': 'https://images.unsplash.com/photo-1570125909232-eb263c188f7e?auto=format&fit=crop&q=80&w=800'},
    ]

    for t in transports:
        image_url = t.pop('image', None)
        obj, created = Transport.objects.update_or_create(name=t['name'], defaults=t)
        if image_url and (created or not obj.image):
            print(f"Downloading image for {t['name']}...")
            img_content = download_image(image_url)
            if img_content:
                obj.image.save(f"{t['name'].replace(' ', '_').lower()}.jpg", img_content, save=True)
                print(f"Saved image for {t['name']}")

    # GUIDES
    guides = [
        {
            'name': 'Rahul Nair',
            'bio': 'Certified guide with 10 years experience in Kerala history, architecture, and temple traditions.',
            'languages': 'English, Malayalam, Hindi',
            'expertise': 'History, Architecture, Temples',
            'daily_rate': 2500,
            'email': 'rahul@keralaguide.com',
            'phone': '9876543210'
        },
        {
            'name': 'Ananya Das',
            'bio': 'Eco-tourism expert specializing in Munnar tea plantations and Periyar wildlife sanctuary.',
            'languages': 'English, Malayalam, Tamil',
            'expertise': 'Nature, Wildlife, Trekking',
            'daily_rate': 2200,
            'email': 'ananya@keralaguide.com',
            'phone': '9876543211'
        },
        {
            'name': 'Vijay Menon',
            'bio': 'Backwater specialist with deep knowledge of Alleppey houseboats and Kuttanad farming.',
            'languages': 'English, Malayalam',
            'expertise': 'Backwaters, Culture, Cuisine',
            'daily_rate': 2000,
            'email': 'vijay@keralaguide.com',
            'phone': '9876543212'
        },
    ]

    for g in guides:
        Guide.objects.get_or_create(name=g['name'], defaults=g)

    print("Kerala data seeded successfully!")

if __name__ == '__main__':
    seed_kerala_data()
