
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_guide_project.settings')
django.setup()

from guide.models import Guide

demo_names = ["Rahul Nair", "Ananya Das", "Vijay Menon"]

for name in demo_names:
    try:
        guide = Guide.objects.filter(name=name).first()
        if guide:
            guide.delete()
            print(f"Deleted demo guide: {name}")
        else:
            print(f"Guide not found: {name}")
    except Exception as e:
        print(f"Error deleting {name}: {e}")

print("Demo guide removal complete.")
