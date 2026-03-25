import os
import django
import sys
import urllib.request
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Transport

def download_image(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return ContentFile(response.read())
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
    return None

def update_transport_images():
    # New high-quality Unsplash images
    transport_images = {
        'Kerala Houseboat': 'https://images.unsplash.com/photo-1593113598332-cd288d649433?q=80&w=2070', # Authentic houseboat
        'Shikara Boat': 'https://images.unsplash.com/photo-1593693411515-c20261bcad6e?q=80&w=2069', # Canoe/small boat vibe
        'Kochi Tourist Cab': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?q=80&w=2070', # Car on road
        'Innova Crysta': 'https://images.unsplash.com/photo-1503376763036-066120622c74?q=80&w=2070', # Luxury car interior/exterior
        'Auto Rickshaw': 'https://images.unsplash.com/photo-1584950746656-3c22b9f390d4?q=80&w=2070', # Classic Tuk-tuk
        'KSRTC Tourist Bus': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=2070', # Bus/Travel vibe
    }

    print("Updating Transport images...")

    for name, url in transport_images.items():
        transport = Transport.objects.filter(name__icontains=name).first()
        if transport:
            print(f"Downloading image for {transport.name}...")
            img_content = download_image(url)
            if img_content:
                # Delete old image if it exists
                if transport.image:
                    transport.image.delete(save=False)
                
                filename = f"{transport.name.replace(' ', '_').lower()}.jpg"
                transport.image.save(filename, img_content, save=True)
                print(f"[OK] Updated image for {transport.name}")
            else:
                print(f"[ERR] Failed to download image for {transport.name}")
        else:
            print(f"[WARN] Transport '{name}' not found in database.")

if __name__ == '__main__':
    update_transport_images()
