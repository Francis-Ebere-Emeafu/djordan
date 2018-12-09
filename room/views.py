from datetime import timedelta, date  # datetime
from decimal import Decimal

from django.contrib import messages
from django.db.models.aggregates import Sum
from django.db.models.functions import (ExtractDay)
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.utils import timezone
from django.views.generic import View

from room.models import Guest, Room, Facility, Booking, HouseKeeping,\
    Requisition, RequisitionMaster, Bill, Inventory, Purchase, PurchaseMaster,\
    Transfer
from room.forms import GuestForm, BookingForm, RequisitionForm, PurchaseForm,\
    TransferForm, GuestChangeForm
from searchdates.daterange import DateSearchForm
from user_profile.utils import render_to_pdf


def guest_list(request):
    guests = Guest.objects.all()
    return render(request, 'room/guest_list.html', {'guests': guests})


def occupied_guest_list(request):
    guests = Guest.objects.all().filter(checked_out=False)
    return render(request, 'room/guest_list.html', {'guests': guests})


def checkedout_guest_list(request):
    guests = Guest.objects.all().filter(checked_out=True)
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


def change_departure_date(request, id):
    # Get instance of a guests details and edit only the departure date incase
    # the guest no longer wants to stay for all the initial dates booked for
    guest = get_object_or_404(Guest, pk=id)
    form = GuestChangeForm(request.POST or None, instance=guest)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('hotel_guest_list')

    return render(request, 'room/change_departure.html', {'form': form})


def paid_check_out(request, id):
    guest = get_object_or_404(Guest, pk=id)
    bills = Bill.objects.filter(guest=guest)
    if guest:
        guest.checked_out = True
        guest.save()

    days = guest.departure_date - guest.arrival_date

    service_bills = bills.aggregate(
        Sum('amount'))['amount__sum'] or Decimal(0)

    if not days.days == 0:
        accomodation_bill = guest.room.room_type.cost * days.days
    else:
        accomodation_bill = guest.room.room_type.cost

    context = {
        'guest': guest,
        'bills': bills,
        'accomodation_bill': accomodation_bill,
        'total': accomodation_bill + service_bills - guest.deposit,
    }
    pdf = render_to_pdf('room/paid_check_out.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("guest.id")
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Document not found")


def pay_check_out(request, id):
    guest = get_object_or_404(Guest, pk=id)
    bills = Bill.objects.filter(guest=guest)
    service_bills = bills.aggregate(
        Sum('amount'))['amount__sum'] or Decimal(0)

    days = guest.departure_date - guest.arrival_date
    if not days.days == 0:
        accomodation_bill = guest.room.room_type.cost * days.days
    else:
        accomodation_bill = guest.room.room_type.cost

    context = {
        'guest': guest,
        'bills': bills,
        'accomodation_bill': accomodation_bill,
        'total': accomodation_bill + service_bills - guest.deposit,
    }
    return render(request, 'room/pay_check_out.html', context)


def pre_check_out(request, id):
    guest = get_object_or_404(Guest, pk=id)
    bills = Bill.objects.filter(guest=guest)
    service_bills = bills.aggregate(
        Sum('amount'))['amount__sum'] or Decimal(0)

    days = guest.departure_date - guest.arrival_date
    if not days.days == 0:
        accomodation_bill = guest.room.room_type.cost * days.days
    else:
        accomodation_bill = guest.room.room_type.cost

    context = {
        'guest': guest,
        'bills': bills,
        'accomodation_bill': accomodation_bill,
        'total': accomodation_bill + service_bills - guest.deposit,
    }
    return render(request, 'room/pre_check_out.html', context)


def get_default_dates():
    end_date = date.today()
    start_date = end_date - timedelta(5)
    return start_date, end_date


def view_room_with_date(request):
    start = request.GET.get('start', None)
    if start:
        form = DateSearchForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start']
            end_date = form.cleaned_data['end']
    else:
        form = DateSearchForm()
        start_date, end_date = get_default_dates()

    _rooms = Guest.objects.filter(
        arrival_date__range=(start_date, end_date), checked_out=False)
    context = {
        'searched_rooms': _rooms,
        'form': form,
    }
    return render(request, 'room/room_with_date.html', context)


def facility_list(request):
    facilities = Facility.objects.all()
    return render(
        request, 'room/facilities.html', {'facilities': facilities})


def booked_facilities(request):
    facilities = Booking.objects.filter(facility__occupied=True)
    if not facilities:
        print ('booked facilities: none')
    return render(
        request, 'room/booked_facilities.html', {'facilities': facilities})


def booking_facility(request):
    # booking_date = timezone.datetime(year, month, day)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            facility = booking.facility
            facility.occupied = True
            facility.save()
            messages.info(request, 'Your facility has been booked')
            return redirect('hotel_facility_list')
    else:
        form = BookingForm()
    return render(request, 'room/booking_facility.html', {'form': form})


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
    # service = service_map[id]
    bills2 = Bill.objects.all()
    for bill in bills2:
        print(bill)
    return render(
        request,
        'room/bills.html',
        {
            'bills': bills,
            'service': 'service'
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


class GeneratePDF(View):
    # Class based function to generate a pdf invoice for
    #  the guest's expenditures
    def get(self, request, id, *args, **kwargs):
        # template = get_template('room/print_bill.html')
        guest = get_object_or_404(Guest, pk=id)
        bills = Bill.objects.filter(guest=guest)
        days = guest.departure_date - guest.arrival_date
        print (type(days))
        print(days)

        service_bills = bills.aggregate(
            Sum('amount'))['amount__sum'] or Decimal(0)

        if not days.days == 0:
            accomodation_bill = guest.room.room_type.cost * days.days
        else:
            accomodation_bill = guest.room.room_type.cost

        context = {
            'guest': guest,
            'bills': bills,
            'accomodation_bill': accomodation_bill,
            'total': accomodation_bill + service_bills - guest.deposit,
        }
        # html = template.render(context)
        pdf = render_to_pdf('room/print_bill.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("guest.id")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Document not found")
