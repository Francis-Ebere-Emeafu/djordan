from django.urls import path

from user_profile import views


urlpatterns = [
    path('admin/', views.admin_profile, name='admin_profile'),
    path('frontdesk/', views.frontdesk_profile, name='frontdesk_profile'),
    path('laundry/', views.laundry_profile, name='laundry_profile'),
    path('laundry/bills', views.guest_bill_list, name='guest_bill_list'),
    path('edit/bill/<int:id>/', views.edit_guest_bill, name='edit_guest_bill'),
    path('store/', views.store_profile, name='store_profile'),
    path('store/outflow', views.stock_outflow, name='stock_outflow'),
    path('store/levels', views.stock_levels, name='stock_levels'),
    path('bar/', views.bar_profile, name='bar_profile'),
    path('restaurant/', views.restaurant_profile, name='restaurant_profile'),
    path('kitchen/', views.kitchen_profile, name='kitchen_profile'),
    # path('newguests/', views.new_guest, name='hotel_new_guest'),
]
