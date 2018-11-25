from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user_profile.models import UserProfile
from user_profile.utils import *


@login_required
def admin_profile(request):
    # if not is_admin(request.user):
    #     logout(request)
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


@login_required
def frontdesk_profile(request):
    profile = UserProfile.objects.get
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


@login_required
def laundry_profile(request):
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


@login_required
def store_profile(request):
    context = {}
    return render(request, 'user_profile/front_desk.html', context)


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
