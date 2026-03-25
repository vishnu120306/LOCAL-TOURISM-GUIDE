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

# New high-quality event images from Unsplash
event_images = {
    'Thrissur Pooram': 'https://images.unsplash.com/photo-1583339793403-3d9b001b6008?auto=format&fit=crop&q=80&w=1200',  # Indian festival with elephants
    'Nehru Trophy Boat Race': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&q=80&w=1200',  # Boat racing
    'Onam Festival': 'https://images.unsplash.com/photo-1604608672516-f1b9b1b7b4d1?auto=format&fit=crop&q=80&w=1200',  # Indian festival celebration
    'Theyyam Performance': 'https://images.unsplash.com/photo-1609619385002-f40f5c9c5d4e?auto=format&fit=crop&q=80&w=1200',  # Traditional Indian performance
    'Cochin Carnival': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?auto=format&fit=crop&q=80&w=1200',  # Carnival celebration
}

def update_event_images():
    # Create media directories if they don't exist
    media_root = 'media'
    events_dir = os.path.join(media_root, 'events')
    os.makedirs(events_dir, exist_ok=True)
    
    print("Starting event image updates...\n")
    
    for event_name, image_url in event_images.items():
        try:
            event = Event.objects.get(name=event_name)
            
            # Create destination filename
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
    update_event_images()
