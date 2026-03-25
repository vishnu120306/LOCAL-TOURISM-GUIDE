import os
import django
import sys
import shutil

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Location, Event, Transport

# Mapping of generated images to copy
image_mappings = {
    'locations': {
        'Munnar Tea Gardens': r'C:/Users/vishn/.gemini/antigravity/brain/8bcb25ab-9ba0-4337-b1d6-f6817796e046/munnar_tea_gardens_1768676704303.png',
        'Alleppey Backwaters': r'C:/Users/vishn/.gemini/antigravity/brain/8bcb25ab-9ba0-4337-b1d6-f6817796e046/alleppey_backwaters_1768676719965.png',
        'Fort Kochi': r'C:/Users/vishn/.gemini/antigravity/brain/8bcb25ab-9ba0-4337-b1d6-f6817796e046/fort_kochi_1768676734390.png',
        'Wayanad Wildlife Sanctuary': r'C:/Users/vishn/.gemini/antigravity/brain/8bcb25ab-9ba0-4337-b1d6-f6817796e046/wayanad_wildlife_1768676751489.png',
        'Periyar National Park': r'C:/Users/vishn/.gemini/antigravity/brain/8bcb25ab-9ba0-4337-b1d6-f6817796e046/periyar_national_park_1768676767988.png',
        'Kovalam Beach': r'C:/Users/vishn/.gemini/antigravity/brain/8bcb25ab-9ba0-4337-b1d6-f6817796e046/kovalam_beach_1768676783658.png',
    }
}

def update_images():
    # Create media directories if they don't exist
    media_root = 'media'
    locations_dir = os.path.join(media_root, 'locations')
    os.makedirs(locations_dir, exist_ok=True)
    
    # Update Location images
    for location_name, source_path in image_mappings['locations'].items():
        try:
            location = Location.objects.get(name=location_name)
            
            # Create destination filename
            dest_filename = f"{location_name.replace(' ', '_').lower()}.png"
            dest_path = os.path.join(locations_dir, dest_filename)
            
            # Copy the image
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                print(f"[OK] Copied image for {location_name}")
                
                # Update the database
                location.image = f'locations/{dest_filename}'
                location.save()
                print(f"[OK] Updated database for {location_name}")
            else:
                print(f"[ERROR] Source image not found: {source_path}")
                
        except Location.DoesNotExist:
            print(f"[ERROR] Location not found: {location_name}")
        except Exception as e:
            print(f"[ERROR] Error updating {location_name}: {e}")
    
    print("\n[DONE] Image update complete!")

if __name__ == '__main__':
    update_images()
