from django.urls import path

from room import views
from room.views import GeneratePDF


urlpatterns = [
    path('guests/', views.guest_list, name='hotel_guest_list'),
    path('occupied/', views.occupied_guest_list, name='occupied_guest_list'),
    path('checkedout/', views.checkedout_guest_list, name='checkedout_guest_list'),
    path('newguests/', views.new_guest, name='hotel_new_guest'),
    path('rooms/', views.room_list, name='hotel_room_list'),
    path('checkout/<int:id>/', views.pre_check_out, name='pre_check_out'),
    path('checkout/<int:id>/pay/', views.pay_check_out, name='pay_check_out'),
    path('checkout/<int:id>/paid/', views.paid_check_out, name='paid_check_out'),
    path('change/<int:id>/', views.change_departure_date, name='change_date'),
    path('facilities/', views.facility_list, name='hotel_facility_list'),
    path('booking/<int:id>/', views.booking, name='hotel_booking'),
    path('facility/booking/', views.booking_facility, name='booking_facility'),
    path('booked/facility', views.booked_facilities, name='booked_facilities'),
    # <int:day>/<int:month>/<int:year>/
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
    path('print/<int:id>/', GeneratePDF.as_view(), name='print_bill_pdf'),
    path('occupied/dates/', views.view_room_with_date, name='view_room_with_date'),
]
