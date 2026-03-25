from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    path('', views.home, name='home'),
    path('start-exploring/', views.start_exploring, name='start_exploring'),
    path('attractions/', views.attractions, name='attractions'),
    path('events/', views.events, name='events'),
    path('explore/', views.explore, name='explore'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('itinerary/<int:itinerary_id>/', views.itinerary_detail, name='itinerary_detail'),
    path('add-review/<str:item_type>/<int:item_id>/', views.add_review, name='add_review'),
    path('guides/', views.guide_list, name='guide_list'),
    path('transports/', views.transport_list, name='transport_list'),
    path('book/<int:guide_id>/', views.book_guide, name='book_guide'),
    path('book-item/<str:item_type>/<int:item_id>/', views.book_item, name='book_item'),
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Search & Bookings
    path('search/', views.search, name='search'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('guide-dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('my-trips/', views.user_bookings, name='user_bookings'),
    path('update-booking-status/<int:booking_id>/<str:action>/', views.update_booking_status, name='update_booking_status'),
    path('sample-trips/', views.sample_trips, name='sample_trips'),
    path('add-location/', views.add_location, name='add_location'),
    path('add-event/', views.add_event, name='add_event'),
    path('add-transport/', views.add_transport, name='add_transport'),
    path('add-itinerary/', views.add_itinerary, name='add_itinerary'),
    path('choose-add-type/', views.choose_content_type, name='choose_add_type'),
    path('guide-profile/', views.guide_profile_management, name='guide_profile_management'),
    path('booking-chat/<int:booking_id>/', views.booking_chat, name='booking_chat'),
]
