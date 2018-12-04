# from datetimewidget.widgets import DateTimeWidget
from django import forms
from datetime import date


# class MyDateField(forms.DateField):
#     widget = DateTimeWidget

#     def __init__(self, *args, **kwargs):
#         super(MyDateField, self).__init__()
#         self.input_formats = ('%Y-%m-%d',)


class DateSearchForm(forms.Form):
    start = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'datepicker'}))
    # MyDateField(initial=date.today)
    end = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'datepicker'}))
    # MyDateField(initial=date.today)

    def __init__(self, *args, **kwargs):
        super(DateSearchForm, self).__init__(*args, **kwargs)
        self.fields['start'].initial = date.today
        self.fields['end'].initial = date.today

    def clean(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data['start']
        if start and end and start > end:
            raise forms.ValidationError(
                'The start date must be before the end date')
        return self.cleaned_data
