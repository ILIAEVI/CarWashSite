from django.forms import ModelForm
from django import forms
from booking.models import Booking, CreateVehicle


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class BookingForm(ModelForm):
    vehicle = forms.ModelChoiceField(queryset=CreateVehicle.objects.all(), empty_label="Select your Vehicle")

    class Meta:
        model = Booking
        fields = ["vehicle", "service", "datetime"]
        widgets = {
            'datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = CreateVehicle.objects.filter(user=user)


class CreateVehicleForm(ModelForm):
    class Meta:
        model = CreateVehicle
        fields = ["brand", "body_shape", "model", "license_plate"]
