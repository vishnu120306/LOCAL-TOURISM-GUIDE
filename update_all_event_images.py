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
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                return ContentFile(response.read())
    except Exception as e:
        print(f"[ERROR] downloading {url}: {e}")
    return None

# New reliable images from Pexels (free to use)
event_images = {
    'Thrissur Pooram': 'https://images.pexels.com/photos/3408354/pexels-photo-3408354.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Indian temple festival
    'Nehru Trophy Boat Race': 'https://images.pexels.com/photos/1659438/pexels-photo-1659438.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Boat on water
    'Onam Festival': 'https://images.pexels.com/photos/1661546/pexels-photo-1661546.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Indian festival celebration
    'Theyyam Performance': 'https://images.pexels.com/photos/3408344/pexels-photo-3408344.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Traditional Indian performance
    'Cochin Carnival': 'https://images.pexels.com/photos/1157557/pexels-photo-1157557.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Carnival/celebration
}

def update_all_event_images():
    media_root = 'media'
    events_dir = os.path.join(media_root, 'events')
    os.makedirs(events_dir, exist_ok=True)
    
    print("=" * 60)
    print("UPDATING ALL CULTURAL EVENT IMAGES")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for event_name, image_url in event_images.items():
        try:
            event = Event.objects.get(name=event_name)
            dest_filename = f"{event_name.replace(' ', '_').lower()}.jpg"
            
            print(f"[{event_name}]")
            print(f"  Downloading from Pexels...")
            
            img_content = download_image(image_url)
            
            if img_content:
                # Delete old image if exists
                if event.image:
                    try:
                        event.image.delete(save=False)
                    except:
                        pass
                
                # Save new image
                event.image.save(dest_filename, img_content, save=True)
                print(f"  [SUCCESS] Image updated!")
                success_count += 1
            else:
                print(f"  [FAILED] Could not download image")
                fail_count += 1
                
        except Event.DoesNotExist:
            print(f"[ERROR] Event not found: {event_name}")
            fail_count += 1
        except Exception as e:
            print(f"[ERROR] {event_name}: {e}")
            fail_count += 1
        
        print()
    
    print("=" * 60)
    print(f"RESULTS: {success_count} successful, {fail_count} failed")
    print("=" * 60)

if __name__ == '__main__':
    update_all_event_images()
