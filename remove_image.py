
import os
import django
from django.core.files.storage import default_storage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Transport

# Find the transport
transport = Transport.objects.filter(image='transport/kerala_houseboat.jpg').first()

if transport:
    old_image_path = transport.image.path
    # Clear the image field
    transport.image = None
    transport.save()
    print(f"Removed image from Transport: {transport.name}")
    
    # Optional: Delete the file if you want to clean up (commented out for safety unless requested)
    # if os.path.exists(old_image_path):
    #     os.remove(old_image_path)
    #     print("Deleted image file.")
else:
    print("Transport with that image not found.")
