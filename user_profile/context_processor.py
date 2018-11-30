from user_profile.utils import *


def logged_in_as(request):
    logged_in_as = 'none'
    if not request.user.is_authenticated:
        print('None is logged in')
        logged_in_as = 'none'
    else:
        if is_admin(user=request.user):
            logged_in_as = 'admin'
            print ('Admin logged in')
        elif is_frontdesk(user=request.user):
            logged_in_as = 'frontdesk'
            print ('Front Desk logged in')
        elif is_laundry(user=request.user):
            logged_in_as = 'laundry'
            print ('Laundry logged in')
        elif is_store(user=request.user):
            logged_in_as = 'store'
            print ('Store logged in')
        elif is_bar(user=request.user):
            logged_in_as = 'bar'
            print ('Bar logged in')
        elif is_restaurant(user=request.user):
            logged_in_as = 'restaurant'
            print ('Restaurant logged in')
        elif is_kitchen(user=request.user):
            logged_in_as = 'kitchen'
            print ('Kitchen logged in')
    return {"logged_in_as": logged_in_as}
