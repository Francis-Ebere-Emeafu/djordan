from django import forms

from room.models import Guest, Room, Booking, Requisition, Purchase,\
    Transfer, Facility, HouseKeeping, Bill, Inventory, Item


class GuestForm(forms.ModelForm):
    queryset = Room.objects.filter(occupied=False)
    room = forms.ModelChoiceField(queryset, empty_label="Select type")
    departure_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'})
    )

    class Meta:
        model = Guest
        exclude = ['checked_out']


class GuestChangeForm(forms.ModelForm):
    departure_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'})
    )

    # def __init__(self, *args, **kwargs):
    #     super(GuestForm, self).__init__(*args, **kwargs)
    #     self.fields['departure_date'].empty_label = "Choose date"

    class Meta:
        model = Guest
        fields = ['surname', 'other_names', 'arrival_date', 'departure_date']
        # widgets = {
        #     'departure_date': forms.DateInput(attrs={'class': 'datepicker'}),
        # }


class CheckoutForm(forms.Form):
    pass


class BookingForm(forms.ModelForm):
    queryset = Facility.objects.all()
    facility = forms.ModelChoiceField(queryset, empty_label="Select Facility")
    booked_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'})
    )

    class Meta:
        model = Booking
        exclude = ['timestamp']

    def clean(self):
        _facility = self.cleaned_data['facility']
        _booked_date = self.cleaned_data['booked_date']
        reservations = Booking.objects.filter(
            booked_date=_booked_date, facility=_facility)
        if reservations:
            print ('reservations stage passed')
            for booked in reservations:
                if booked.facility.occupied:
                    print ('date is in use')
                    raise forms.ValidationError('Date already in use')


class RequisitionForm(forms.ModelForm):
    queryset = HouseKeeping.objects.all()
    item = forms.ModelChoiceField(queryset, empty_label="Select housekeeping item")

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


class BillForm(forms.ModelForm):
    queryset = Guest.objects.filter(checked_out=False)
    guest = forms.ModelChoiceField(queryset, empty_label='select guest')
    bill_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = Bill
        exclude = ['service']


class InventoryForm(forms.ModelForm):
    queryset = Item.objects.all()
    item = forms.ModelChoiceField(queryset, empty_label='Select Item')

    class Meta:
        model = Inventory
        exclude = ['location']


class InventoryOutflowForm(forms.ModelForm):
    queryset = Item.objects.all()
    item = forms.ModelChoiceField(queryset, empty_label='Select Item')

    class Meta:
        model = Inventory
        exclude = []

    def clean_location(self):
        if 'location' in self.cleaned_data:
            if self.cleaned_data['location'] == 4:
                raise forms.ValidationError('Select a valid location')
        return self.cleaned_data['location']
