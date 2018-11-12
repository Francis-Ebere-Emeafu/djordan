from django.contrib import admin

from room.models import RoomType, Room, CompanyAccount, Guest, Facility,\
    Booking, HouseKeeping, Requisition, Bill, Item, Inventory, Transfer



@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'occupied']


@admin.register(CompanyAccount)
class CompanyAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'balance']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['surname', 'other_names', 'room', 'deposit']


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['facility', 'booked_date', 'amount']


@admin.register(HouseKeeping)
class HouseKeepingAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate', 'quantity']


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ['item', 'rate', 'quantity']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['amount', 'bill_date', 'paid', 'description', 'guest']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'location']


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['item', 'destination', 'quantity', 'when']
