from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from user_profile.models import UserProfile
from user_profile.utils import *

from room.models import Bill, Inventory
from room.forms import BillForm, InventoryForm, InventoryOutflowForm


@login_required
def admin_profile(request):
    # if not is_admin(request.user):
    #     logout(request)
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


@login_required
def frontdesk_profile(request):
    # profile = UserProfile.objects.get
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


@login_required
def laundry_profile(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            newbill = form.save(commit=False)
            newbill.service = 3
            newbill.save()
            messages.info(request, 'Bill Entered Successfully')
            return redirect('laundry_profile')
    else:
        form = BillForm()
    context = {'form': form}
    return render(request, 'laundry/laundry.html', context)
    # return render(request, 'user_profile/front_desk.html', context)


def guest_bill_list(request):
    bills = Bill.objects.filter(service=3, paid=False)
    return render(request, 'laundry/bill_list.html', {'bills': bills})


def edit_guest_bill(request, id):
    bill = get_object_or_404(Bill, pk=id)
    form = BillForm(request.POST or None, instance=bill)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('guest_bill_list')
    return render(request, 'laundry/edit_bill.html', {'form': form})


@login_required
def store_profile(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            new_inventory = form.save(commit=False)
            new_inventory.location = 3
            new_inventory.save()
            messages.info(request, 'Inventory Successfully Saved')
            return redirect('store_profile')
    else:
        form = InventoryForm()
    context = {'form': form}
    return render(request, 'store/store.html', context)


def stock_outflow(request):
    if request.method == 'POST':
        form = InventoryOutflowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Stock movement has been recorded')
            return redirect('stock_outflow')
    else:
        form = InventoryOutflowForm()
    context = form = {'form': form}
    return render(request, 'store/stock_outflow.html', context)


def stock_levels(request):
    stock = Inventory.objects.all()
    context = {'stock': stock}
    return render(request, 'store/stock_levels.html', context)


@login_required
def bar_profile(request):
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


@login_required
def restaurant_profile(request):
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


@login_required
def kitchen_profile(request):
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


"""
class SearchSubmitView(View):
    template = 'laundry/search_submit.html'
    respnse_message = 'This is the response'

    def post(self, request):
        template = loader.get_template(self.template)
        query = request.POST.get('search', '')

        # A simple query for Item objects whose title contains 'query'
        items = Item.objects.filter(title__icontains=query)
        context = {'title': self.response_message, 'query': query, 'items': items}

        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template, content_type='text/html')
"""
