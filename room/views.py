from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from room.models import Guest, Room, Facility, Booking, HouseKeeping,\
    Requisition, RequisitionMaster, Bill, Inventory, Purchase, PurchaseMaster,\
    Transfer
from room.forms import GuestForm, BookingForm, RequisitionForm, PurchaseForm,\
    TransferForm


def guest_list(request):
    guests = Guest.objects.all()
    return render(request, 'room/guest_list.html', {'guests': guests})


def new_guest(request):
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save()
            room = guest.room
            room.occupied = True
            room.save()
            messages.info(request, 'Saved Successfully')
            return redirect('hotel_new_guest')
    else:
        form = GuestForm()
    return render(request, 'room/new_guest.html', {'form': form})


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room/room_list.html', {'rooms': rooms})


def check_out(request, id):
    guest = get_object_or_404(Guest, pk=id)
    return render(request, 'room/check_out.html', {'guest': guest})


def facility_list(request):
    facilities = Facility.objects.all()
    return render(
        request, 'room/facilities.html', {'facilities': facilities})


def new_booking(request, day, month, year):
    #booking_date = timezone.datetime(year, month, day)
    form = BookingForm()
    return render(request, 'room/new_booking.html', {'form': form})


def booking(request, id):
    facility = get_object_or_404(Facility, pk=id)
    today = timezone.now()
    events = Booking.objects.all()
    context = {
        'event_list': events,
        'year': today.year,
        'month': today.month,
        'facility': facility
    }
    return render(request, 'room/booking.html', context)


def housekeeping(request):
    items = HouseKeeping.objects.all()
    return render(request, 'room/house_keeping.html', {'items': items})


def new_requisition(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            master = RequisitionMaster.objects.create()
            req.master = master
            req.save()
            messages.info(request, 'Saved requisition')
            return redirect('hotel_requisition', id=master.id)
    else:
        form = RequisitionForm()
    return render(
        request,
        'room/requisition.html',
        {
            'form': form,
            'requisitions': Requisition.objects.none()
        })

def requisition(request, id):
    master = get_object_or_404(RequisitionMaster, pk=id)
    requisitions = Requisition.objects.filter(master__id=id)

    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.master = master
            req.save()
            messages.info(request, 'Saved requisition')
            return redirect('hotel_requisition', id=master.id)
    else:
        form = RequisitionForm()
    return render(
        request,
        'room/requisition.html',
        {
            'form': form,
            'requisitions': requisitions
        })


service_map = {
    '0': 'Restaurant',
    '1': 'Main Bar',
    '2': 'Pool Bar',
    '3': 'Laundry',
    '4': 'Gym'
}


location_map = {
    '0': 'Restaurant',
    '1': 'Main Bar',
    '2': 'Pool Bar',
    '3': 'Store',
}


def bills(request, id):
    bills = Bill.objects.filter(service=id)
    service = service_map[id]
    return render(
        request,
        'room/bills.html',
        {
            'bills': bills,
            'service': service
        }
    )


def inventory(request, id):
    inv = Inventory.objects.filter(location=id)
    location = location_map[id]
    return render(
        request,
        'room/inventory.html',
        {
            'items': inv,
            'location': location
        }
    )


def new_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purc = form.save(commit=False)
            master = PurchaseMaster.objects.create()
            purc.master = master
            purc.save()
            try:
                inv = Inventory.objects.get(
                    item=purc.item, location=Inventory.STORE)
            except Inventory.DoesNotExist:
                Inventory.objects.create(
                    item=purc.item,
                    location=Inventory.STORE,
                    quantity=purc.quantity
                )
            else:
                inv.quantity += purc.quantity
                inv.save()

            messages.info(request, 'Saved purchase')
            return redirect('hotel_purchase', id=master.id)
    else:
        form = PurchaseForm()
    return render(
        request,
        'room/purchase.html',
        {
            'form': form,
            'purchases': Purchase.objects.none()
        })


def purchase(request, id):
    master = get_object_or_404(PurchaseMaster, pk=id)
    purchases = Purchase.objects.filter(master__id=id)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purc = form.save(commit=False)
            purc.master = master
            purc.save()
            try:
                inv = Inventory.objects.get(
                    item=purc.item, location=Inventory.STORE)
            except Inventory.DoesNotExist:
                Inventory.objects.create(
                    item=purc.item,
                    location=Inventory.STORE,
                    quantity=purc.quantity
                )
            else:
                inv.quantity += purc.quantity
                inv.save()

            messages.info(request, 'Saved purchase')
            return redirect('hotel_purchase', id=master.id)
    else:
        form = PurchaseForm()
    return render(
        request,
        'room/purchase.html',
        {
            'form': form,
            'purchases': purchases
        })


def transfer(request):
    disbursements = Transfer.objects.all()
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            trans = form.save()

            inv = Inventory.objects.get(item=trans.item, location=Inventory.STORE)
            try:
                inv_to = Inventory.objects.get(
                    item=trans.item,
                    location=trans.destination)
            except Inventory.DoesNotExist:
                inv_to = Inventory.objects.create(
                    item=trans.item,
                    location=trans.destination,
                    quantity=0)

            inv_to.quantity += trans.quantity
            inv_to.save()

            inv.quantity -= trans.quantity
            inv.save()
            messages.info(request, 'Saved Disbursement')
            return redirect('hotel_transfer')

    else:
        form = TransferForm()
    return render(
        request,
        'room/disbursement.html',
        {
            'form': form,
            'transfers': disbursements
        }
    )
