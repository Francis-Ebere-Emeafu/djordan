from django import forms

from room.models import Guest, Room, Booking, Requisition, Purchase,\
    Transfer


class GuestForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.filter(occupied=False))

    class Meta:
        model = Guest
        exclude = ['checked_out']


class CheckoutForm(forms.Form):
    pass


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        exclude = []


class RequisitionForm(forms.ModelForm):

    class Meta:
        model = Requisition
        exclude = ['master']


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        exclude = ['master']


class TransferForm(forms.ModelForm):

    class Meta:
        model = Transfer
        exclude = ['when']
