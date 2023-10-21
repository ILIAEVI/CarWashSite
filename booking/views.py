from django.shortcuts import render, redirect
from booking.forms import CreateVehicleForm, BookingForm
from django.contrib import messages
from .models import *


def vehicle_create_view(request):
    if request.method == "POST":
        form = CreateVehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            license_plate = form.cleaned_data['license_plate']
            if not CreateVehicle.objects.filter(license_plate=license_plate).exists():
                vehicle.save()
                messages.success(request, 'Vehicle is successfully added')
                return redirect('book_visit')
            else:
                messages.error(request, 'Vehicle with this License Plate already added')

    else:
        form = CreateVehicleForm()
    return render(request, 'create-vehicle.html', {'form': form})


def book_visit_view(request):
    if request.method == "POST":
        form = BookingForm(request.user, request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            datetime = form.cleaned_data['datetime']
            if not Booking.objects.filter(datetime=datetime).exists():
                booking.save()
                messages.success(request, 'Successfully booked')
                return redirect('home')
            else:
                messages.error(request, "This Date is already booked, please choose another one")
    else:
        form = BookingForm(request.user)
    return render(request, 'booking.html', {'form': form})
