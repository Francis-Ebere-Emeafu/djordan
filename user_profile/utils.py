from user_profile.models import UserProfile


def is_admin(user):
    person = UserProfile.objects.get(user=user)
    print(person.usertype)
    if person.usertype == 'admin':
        return True
    return False


def is_frontdesk(user):
    person = UserProfile.objects.get(user=user)
    print(person.usertype)
    if person.usertype == 'frontdesk':
        return True
    return False


def is_laundry(user):
    person = UserProfile.objects.get(user=user)
    print(person.usertype)
    if person.usertype == 'laundry':
        return True
    return False


def is_store(user):
    person = UserProfile.objects.get(user=user)
    print(person.usertype)
    if person.usertype == 'store':
        return True
    return False


def is_bar(user):
    person = UserProfile.objects.get(user=user)
    print(person.usertype)
    if person.usertype == 'bar':
        return True
    return False


def is_restaurant(user):
    person = UserProfile.objects.get(user=user)
    print(person.usertype)
    if person.usertype == 'restaurant':
        return True
    return False


def is_kitchen(user):
    person = UserProfile.objects.get(user=user)
    print(person.usertype)
    if person.usertype == 'kitchen':
        return True
    return False
