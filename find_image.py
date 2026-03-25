
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Transport

# Search for the image
transports = Transport.objects.filter(image__icontains='kerala_houseboat')

if transports.exists():
    for t in transports:
        print(f"Found Transport: ID={t.id}, Name='{t.name}', Image='{t.image}'")
else:
    print("No transport found with that image name.")
