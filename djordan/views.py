from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from user_profile.utils import *


@login_required
def home(request):
    if is_admin(request.user):
        return redirect('admin_profile')
    elif is_frontdesk(request.user):
        # frontdesk_profile
        return redirect('hotel_guest_list')
    elif is_laundry(request.user):
        return redirect('laundry_profile')
    elif is_store(request.user):
        return redirect('store_profile')
    elif is_bar(request.user):
        return redirect('bar_profile')
    elif is_restaurant(request.user):
        return redirect('restaurant_profile')
    elif is_kitchen(request.user):
        return redirect('kitchen_profile')
    else:
        return redirect('login')
