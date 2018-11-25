from django.urls import path

from room import views


urlpatterns = [
    path('guests/', views.guest_list, name='hotel_guest_list'),
    path('newguests/', views.new_guest, name='hotel_new_guest'),
    path('rooms/', views.room_list, name='hotel_room_list'),
    path('checkout/<int:id>/', views.check_out, name='hotel_check_out'),
    path('facilities/', views.facility_list, name='hotel_facility_list'),
    path('booking/<int:id>/', views.booking, name='hotel_booking'),
    path('new_booking/<int:day>/<int:month>/<int:year>/',
         views.new_booking, name='hotel_new_booking'),
    path('housekeeping/',
         views.housekeeping, name='hotel_housekeeping_list'),
    path('requisition/<int:id>/',
         views.requisition, name='hotel_requisition'),
    path('requisition/', views.new_requisition, name='hotel_requisition_new'),
    path('bill/<int:id>/', views.bills, name='hotel_bill_list'),
    path('inventory/<int:id>/', views.inventory, name='hotel_inventory_list'),
    path('purchase/<int:id>/', views.purchase, name='hotel_purchase'),
    path('purchase/', views.new_purchase, name='hotel_purchase_new'),
    path('transfer/', views.transfer, name='hotel_transfer'),
]
