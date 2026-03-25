from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from .forms import SearchForm, BookingForm, UserRegisterForm, LocationForm, EventForm, TransportForm, ItineraryForm, ReviewForm
from .models import Category, Location, Event, Guide, Booking, Itinerary, Transport, ChatMessage, Review

from django.db.models import Avg

def home(request):
    filter_type = request.GET.get('filter', 'all')
    locations = Location.objects.annotate(average_rating=Avg('reviews__rating'))
    events = Event.objects.annotate(average_rating=Avg('reviews__rating'))
    transports = Transport.objects.all()
    
    bookings = []
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(
            Q(user_email=request.user.email) | Q(user_name=request.user.username)
        ).order_by('-created_at')[:3]
    
    return render(request, 'guide/home.html', {
        'locations': locations,
        'events': events,
        'transports': transports,
        'filter': filter_type,
        'bookings': bookings
    })

def start_exploring(request):
    locations = Location.objects.all()
    events = Event.objects.all().order_by('start_date')
    return render(request, 'guide/start_exploring.html', {
        'locations': locations,
        'events': events
    })

def attractions(request):
    locations = Location.objects.annotate(average_rating=Avg('reviews__rating'))
    return render(request, 'guide/attractions.html', {
        'locations': locations
    })

def events(request):
    events = Event.objects.annotate(average_rating=Avg('reviews__rating')).order_by('start_date')
    return render(request, 'guide/events.html', {
        'events': events
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = event.reviews.all()
    return render(request, 'guide/event_detail.html', {
        'event': event,
        'reviews': reviews
    })

def itinerary_detail(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    reviews = itinerary.reviews.all()
    return render(request, 'guide/itinerary_detail.html', {
        'itinerary': itinerary,
        'reviews': reviews
    })

def explore(request):
    filter_type = request.GET.get('filter', 'all')
    locations = Location.objects.all()
    events = Event.objects.all()
    transports = Transport.objects.all()
    return render(request, 'guide/explore.html', {
        'locations': locations,
        'events': events,
        'transports': transports,
        'filter': filter_type
    })

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    locations = category.locations.all()
    return render(request, 'guide/category_detail.html', {
        'category': category,
        'locations': locations
    })

def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    reviews = location.reviews.all()
    events = location.events.all()
    guides = Guide.objects.all()
    return render(request, 'guide/location_detail.html', {
        'location': location,
        'reviews': reviews,
        'events': events,
        'guides': guides
    })

def guide_list(request):
    guides = Guide.objects.all()
    return render(request, 'guide/guide_list.html', {'guides': guides})

def transport_list(request):
    transports = Transport.objects.all()
    return render(request, 'guide/transport_list.html', {'transports': transports})

def book_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    locations = Location.objects.all()
    events = Event.objects.all()
    transports = Transport.objects.all()

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        location_id = request.POST.get('location')
        event_id = request.POST.get('event')
        transport_id = request.POST.get('transport')
        date = request.POST.get('date')

        booking = Booking.objects.create(
            user_name=user_name,
            user_email=user_email,
            guide=guide,
            date=date
        )
        if location_id:
            booking.location = Location.objects.get(id=location_id)
        if event_id:
            booking.event = Event.objects.get(id=event_id)
        if transport_id:
            booking.transport = Transport.objects.get(id=transport_id)
        
        booking.save()
        messages.success(request, f"Successfully booked {guide.name} for {date}!")
        return redirect('guide:user_bookings')

    return render(request, 'guide/book_guide.html', {
        'guide': guide,
        'locations': locations,
        'events': events,
        'transports': transports
    })

@login_required
def book_item(request, item_type, item_id):
    booking_item = None
    guides = Guide.objects.all()
    
    if item_type == 'attraction':
        booking_item = get_object_or_404(Location, id=item_id)
    elif item_type == 'event':
        booking_item = get_object_or_404(Event, id=item_id)
    elif item_type == 'transport':
        booking_item = get_object_or_404(Transport, id=item_id)
    elif item_type == 'trip':
        booking_item = get_object_or_404(Itinerary, id=item_id)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        guide_id = request.POST.get('guide')
        
        booking = Booking.objects.create(
            user_name=request.user.username,
            user_email=request.user.email,
            date=date,
            status='PENDING'
        )
        
        if guide_id:
            booking.guide = Guide.objects.get(id=guide_id)
        else:
            # Auto-assign a random guide so they get the notification
            random_guide = Guide.objects.order_by('?').first()
            if random_guide:
                booking.guide = random_guide
            
        if item_type == 'attraction':
            booking.location = booking_item
        elif item_type == 'event':
            booking.event = booking_item
        elif item_type == 'transport':
            booking.transport = booking_item
        elif item_type == 'trip':
            booking.itinerary_name = booking_item.name
            
        booking.save()
        messages.success(request, f"Successfully booked {booking_item.name}!")
        return redirect('guide:user_bookings')
        
    return render(request, 'guide/book_item.html', {
        'item': booking_item,
        'type': item_type,
        'guides': guides
    })

# ===================== AUTHENTICATION =====================

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check for is_guide
            if form.cleaned_data.get('is_guide'):
                Guide.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email
                )
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('guide:home')
    else:
        form = UserRegisterForm()
    return render(request, 'guide/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('guide:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'guide/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('guide:home')

# ===================== SEARCH =====================

def search(request):
    query = request.GET.get('q', '')
    locations = Location.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(address__icontains=query)
    ) if query else []
    events = Event.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else []
    guides = Guide.objects.filter(
        Q(name__icontains=query) | Q(expertise__icontains=query) | Q(bio__icontains=query)
    ) if query else []
    
    return render(request, 'guide/search_results.html', {
        'query': query,
        'locations': locations,
        'events': events,
        'guides': guides
    })

# ===================== MY BOOKINGS =====================

@login_required
def my_bookings(request):
    # Fetch incoming notifications if the user is a guide
    notifications = []
    is_guide = False
    guide = None
    
    # Try direct profile link first
    if hasattr(request.user, 'guide_profile'):
        guide = request.user.guide_profile
    else:
        # Fallback: search by name or email
        guide = Guide.objects.filter(Q(name=request.user.username) | Q(email=request.user.email)).first()
        if guide and not guide.user:
            # Auto-link the profile if it matches and isn't linked yet
            guide.user = request.user
            guide.save()

    if guide:
        notifications = Booking.objects.filter(guide=guide).order_by('-created_at')
        is_guide = True

    return render(request, 'guide/my_bookings.html', {
        'notifications': notifications,
        'is_guide': is_guide
    })

@login_required
def user_bookings(request):
    # Fetch bookings for the logged-in user
    bookings = Booking.objects.filter(
        Q(user_email=request.user.email) | Q(user_name=request.user.username)
    ).order_by('-created_at')
    
    return render(request, 'guide/user_bookings.html', {
        'bookings': bookings
    })

@login_required
def update_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    
    is_guide = hasattr(request.user, 'guide_profile') and booking.guide == request.user.guide_profile
    is_owner = (booking.user_email == request.user.email) or (booking.user_name == request.user.username)

    # Permission check: Only the guide or the traveler can manage this booking
    if not (is_guide or is_owner):
        messages.error(request, "You are not authorized to manage this booking.")
        return redirect('guide:home')

    if action == 'confirm':
        if not is_guide:
            messages.error(request, "Only guides can confirm bookings.")
        else:
            booking.status = 'CONFIRMED'
            messages.success(request, f"Booking for {booking.user_name} has been confirmed.")
    elif action == 'cancel':
        booking.status = 'CANCELLED'
        if is_guide:
            messages.warning(request, f"Booking for {booking.user_name} has been cancelled by the guide.")
        else:
            messages.info(request, "Your booking has been cancelled.")
    
    booking.save()
    
    # Redirect back to the page the user came from
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('guide:guide_dashboard')

@login_required
def guide_dashboard(request):
    guide = None
    # Try direct profile link first
    if hasattr(request.user, 'guide_profile'):
        guide = request.user.guide_profile
    else:
        # Fallback: search by name or email
        guide = Guide.objects.filter(Q(name=request.user.username) | Q(email=request.user.email)).first()
        if guide and not guide.user:
            # Auto-link the profile if it matches and isn't linked yet
            guide.user = request.user
            guide.save()

    if not guide:
        messages.error(request, "You do not have a guide profile. Please register as a guide to access the dashboard.")
        return redirect('guide:home')

    bookings = Booking.objects.filter(guide=guide).order_by('-created_at')
    return render(request, 'guide/guide_dashboard.html', {
        'guide': guide,
        'bookings': bookings
    })

@login_required
def add_location(request):
    if not hasattr(request.user, 'guide_profile'):
        messages.error(request, "Only registered guides can add new locations.")
        return redirect('guide:home')
    
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.save()
            messages.success(request, f"Successfully added {location.name}!")
            return redirect('guide:guide_dashboard')
    else:
        form = LocationForm()
    
    return render(request, 'guide/add_location.html', {'form': form})

@login_required
def add_event(request):
    if not hasattr(request.user, 'guide_profile'):
        messages.error(request, "Only registered guides can add new events.")
        return redirect('guide:home')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Successfully added {event.name}!")
            return redirect('guide:guide_dashboard')
    else:
        form = EventForm()
    
    return render(request, 'guide/add_event.html', {'form': form})

@login_required
def add_transport(request):
    if not hasattr(request.user, 'guide_profile'):
        messages.error(request, "Only registered guides can add transport services.")
        return redirect('guide:home')
    
    if request.method == 'POST':
        form = TransportForm(request.POST, request.FILES)
        if form.is_valid():
            transport = form.save()
            messages.success(request, f"Successfully added {transport.name}!")
            return redirect('guide:guide_dashboard')
    else:
        form = TransportForm()
    
    return render(request, 'guide/add_transport.html', {'form': form})

@login_required
def add_itinerary(request):
    if not hasattr(request.user, 'guide_profile'):
        messages.error(request, "Only registered guides can add new itineraries.")
        return redirect('guide:home')
    
    if request.method == 'POST':
        form = ItineraryForm(request.POST, request.FILES)
        if form.is_valid():
            itinerary = form.save()
            messages.success(request, f"Successfully added {itinerary.name}!")
            return redirect('guide:guide_dashboard')
    else:
        form = ItineraryForm()
    
    return render(request, 'guide/add_itinerary.html', {'form': form})

@login_required
def choose_content_type(request):
    if not hasattr(request.user, 'guide_profile'):
        messages.error(request, "Only registered guides can contribute content.")
        return redirect('guide:home')
    return render(request, 'guide/choose_content_type.html')

def sample_trips(request):
    itineraries = Itinerary.objects.all()
    return render(request, 'guide/sample_trips.html', {
        'itineraries': itineraries
    })

@login_required
def add_review(request, item_type, item_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(
                user_name=request.user.username,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )
            
            if item_type == 'attraction':
                review.location = get_object_or_404(Location, id=item_id)
            elif item_type == 'event':
                review.event = get_object_or_404(Event, id=item_id)
            elif item_type == 'itinerary':
                review.itinerary = get_object_or_404(Itinerary, id=item_id)
            
            review.save()
            messages.success(request, "Review added successfully!")
    
    # Redirect back to the referrer
    return redirect(request.META.get('HTTP_REFERER', 'guide:home'))

@login_required
def guide_profile_management(request):
    # Get or create guide profile
    guide = None
    if hasattr(request.user, 'guide_profile'):
        guide = request.user.guide_profile
    else:
        # Fallback: search by name or email
        guide = Guide.objects.filter(Q(name=request.user.username) | Q(email=request.user.email)).first()
        if guide and not guide.user:
            guide.user = request.user
            guide.save()
    
    if not guide:
        messages.error(request, "You do not have a guide profile. Please register as a guide to access profile management.")
        return redirect('guide:home')
    
    if request.method == 'POST':
        # Update guide profile
        guide.name = request.POST.get('name', guide.name)
        guide.bio = request.POST.get('bio', guide.bio)
        guide.languages = request.POST.get('languages', guide.languages)
        guide.expertise = request.POST.get('expertise', guide.expertise)
        guide.phone = request.POST.get('phone', guide.phone)
        guide.email = request.POST.get('email', guide.email)
        
        # Handle daily rate
        daily_rate = request.POST.get('daily_rate')
        if daily_rate:
            try:
                guide.daily_rate = float(daily_rate)
            except ValueError:
                pass
        
        # Handle image upload
        if request.FILES.get('image'):
            guide.image = request.FILES['image']
        
        guide.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('guide:guide_profile_management')
    
    return render(request, 'guide/guide_profile_management.html', {
        'guide': guide
    })

@login_required
def booking_chat(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Access Control: Only guide or user related to booking
    is_guide = hasattr(request.user, 'guide_profile') and booking.guide == request.user.guide_profile
    is_user = (booking.user_email == request.user.email) or (booking.user_name == request.user.username)
    
    if not (is_guide or is_user):
        messages.error(request, "Access denied.")
        return redirect('guide:home')

    if booking.status != 'CONFIRMED':
        messages.warning(request, "Chat is only available for confirmed bookings.")
        return redirect('guide:home')

    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content and message_content.strip():
            print(f"DEBUG: Processing message from {request.user.username} for booking {booking_id}")
            ChatMessage.objects.create(
                booking=booking,
                sender=request.user,
                message=message_content
            )
            # No success message to keep chat flow fluid, but verify redirect works
            return redirect('guide:booking_chat', booking_id=booking_id)

    # Mark messages as read
    # Logic to mark as read could go here
    # e.g., messages.filter(sender!=request.user, is_read=False).update(is_read=True)
    
    messages_list = booking.messages.all()

    return render(request, 'guide/booking_chat.html', {
        'booking': booking,
        'chat_messages': messages_list,
        'is_guide': is_guide
    })

