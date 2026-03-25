from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location, Event, Category, Transport, Itinerary

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_guide = forms.BooleanField(required=False, label="Register as a Guide")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookingForm(forms.Form):
    user_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Your Name'
    }))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'Your Email'
    }))
    location = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'form-input'
    }))
    transport = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'form-input'
    }))
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-input',
        'type': 'date'
    }))

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'search-input',
        'placeholder': 'Search attractions, events, guides...'
    }))

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['category', 'name', 'description', 'image', 'address', 'latitude', 'longitude', 'website', 'phone']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Attraction Name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe this place...', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Address'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Latitude (Optional)'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Longitude (Optional)'}),
            'website': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Website URL (Optional)'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Contact Phone (Optional)'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'start_date', 'end_date', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the event...', 'rows': 4}),
            'location': forms.Select(attrs={'class': 'form-input'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
        }

class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ['name', 'transport_type', 'description', 'image', 'price_per_km']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Transport Name (e.g. Golden Taxi)'}),
            'transport_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe your service...', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            'price_per_km': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Price per Kilometer'}),
        }

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['name', 'description', 'image', 'duration', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Trip Name (e.g. Munnar Escape)'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'What is included in this trip?', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            'duration': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 2 Days, 1 Night'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Total Trip Cost'}),
        }

class ReviewForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=5, 
        widget=forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'max': '5'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Share your experience...', 'rows': 4})
    )
