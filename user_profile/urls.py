from django.urls import path

from user_profile import views


urlpatterns = [
    path('admin/', views.admin_profile, name='admin_profile'),
    path('frontdesk/', views.frontdesk_profile, name='frontdesk_profile'),
    path('laundry/', views.laundry_profile, name='laundry_profile'),
    path('store/', views.store_profile, name='store_profile'),
    path('bar/', views.bar_profile, name='bar_profile'),
    path('restaurant/', views.restaurant_profile, name='restaurant_profile'),
    path('kitchen/', views.kitchen_profile, name='kitchen_profile'),
    # path('newguests/', views.new_guest, name='hotel_new_guest'),
]
