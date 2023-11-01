from django.forms import ModelForm
from django import forms
from booking.models import Booking, Vehicle


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class BookingForm(ModelForm):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all(), empty_label="Select your Vehicle")

    class Meta:
        model = Booking
        fields = ["vehicle", "service", "datetime"]
        widgets = {
            'datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)


class VehicleForm(ModelForm):

    class Meta:
        model = Vehicle
        fields = ["nickname", "brand", "body_shape", "model", "license_plate", "image"]


'''

class VehicleDisplayForm(ModelForm):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all(), empty_label="Select your Vehicle")

    class Meta:
        model = Booking
        fields = ['vehicle']

    def __init__(self, user, *args, **kwargs):
        super(VehicleDisplayForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)

'''
