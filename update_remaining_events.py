import os
import django
import sys
import urllib.request
from django.core.files.base import ContentFile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Event

def download_image(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return ContentFile(response.read())
    except Exception as e:
        print(f"[ERROR] downloading image {url}: {e}")
    return None

# Using more reliable Unsplash URLs
event_images = {
    'Onam Festival': 'https://images.unsplash.com/photo-1514525253440-b39b56360c49?w=800&auto=format&fit=crop',  # Festival celebration
    'Theyyam Performance': 'https://images.unsplash.com/photo-1567157577861-53625f2066d7?w=800&auto=format&fit=crop',  # Traditional dance/performance
}

def update_final_events():
    media_root = 'media'
    events_dir = os.path.join(media_root, 'events')
    os.makedirs(events_dir, exist_ok=True)
    
    print("Final attempt to update event images...\n")
    
    for event_name, image_url in event_images.items():
        try:
            event = Event.objects.get(name=event_name)
            dest_filename = f"{event_name.replace(' ', '_').lower()}.jpg"
            
            print(f"Downloading image for {event_name}...")
            img_content = download_image(image_url)
            
            if img_content:
                event.image.save(dest_filename, img_content, save=True)
                print(f"[OK] Updated {event_name}")
            else:
                print(f"[ERROR] Failed to download image for {event_name}")
                
        except Event.DoesNotExist:
            print(f"[ERROR] Event not found: {event_name}")
        except Exception as e:
            print(f"[ERROR] Error updating {event_name}: {e}")
    
    print("\n[DONE] Event image update complete!")

if __name__ == '__main__':
    update_final_events()
