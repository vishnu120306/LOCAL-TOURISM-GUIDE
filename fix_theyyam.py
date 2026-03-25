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
        print(f"[ERROR] downloading: {e}")
    return None

# Alternative image for Theyyam Performance
event_name = 'Theyyam Performance'
# Try multiple URLs
image_urls = [
    'https://images.pexels.com/photos/3408353/pexels-photo-3408353.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Indian cultural performance
    'https://images.pexels.com/photos/1661546/pexels-photo-1661546.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Traditional festival
    'https://images.pexels.com/photos/2526105/pexels-photo-2526105.jpeg?auto=compress&cs=tinysrgb&w=1200',  # Cultural dance
]

def update_theyyam():
    print(f"Updating {event_name}...")
    
    try:
        event = Event.objects.get(name=event_name)
        dest_filename = f"{event_name.replace(' ', '_').lower()}.jpg"
        
        for i, image_url in enumerate(image_urls, 1):
            print(f"  Trying URL {i}/{len(image_urls)}...")
            img_content = download_image(image_url)
            
            if img_content:
                if event.image:
                    try:
                        event.image.delete(save=False)
                    except:
                        pass
                
                event.image.save(dest_filename, img_content, save=True)
                print(f"  [SUCCESS] {event_name} image updated!")
                return True
        
        print(f"  [FAILED] All URLs failed for {event_name}")
        return False
                
    except Event.DoesNotExist:
        print(f"[ERROR] Event not found: {event_name}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == '__main__':
    update_theyyam()
