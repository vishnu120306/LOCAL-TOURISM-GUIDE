from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    description = models.TextField(blank=True)

    def __cl__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Location(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='locations/', blank=True, null=True)
    address = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    itinerary = models.ForeignKey('Itinerary', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.location or self.event or self.itinerary
        target_name = target.name if target else "Unknown"
        return f"{self.user_name} - {target_name} ({self.rating})"

class Transport(models.Model):
    TRANSPORT_TYPES = [
        ('BOAT', 'Houseboat'),
        ('TAXI', 'Taxi/Cab'),
        ('TUKTUK', 'Auto Rickshaw'),
        ('BUS', 'Tourist Bus'),
    ]
    name = models.CharField(max_length=100)
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='transport/', blank=True, null=True)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.get_transport_type_display()})"

class Itinerary(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='itineraries/', blank=True, null=True)
    duration = models.CharField(max_length=100, help_text="e.g. 3 Days, 2 Nights")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='guide_profile')
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='guides/', blank=True, null=True)
    languages = models.CharField(max_length=200, help_text="Comma separated languages", blank=True)
    expertise = models.CharField(max_length=200, help_text="e.g. History, Nature, Culture", blank=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default=800.00)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    transport = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True, blank=True)
    itinerary_name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        guide_name = self.guide.name if self.guide else "No Guide"
        return f"Booking by {self.user_name} for {guide_name} on {self.date}"

class ChatMessage(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

