from django.contrib.auth.models import User
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from user_profile.models import UserProfile


def is_admin(user):
    person = User.objects.get(username=user)
    if person.is_superuser:
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


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
