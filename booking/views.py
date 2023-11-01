from django.shortcuts import render, redirect, get_object_or_404
from booking.forms import VehicleForm, BookingForm
from django.contrib import messages
from .models import Vehicle, Booking


def display_all_vehicles(request):
    user = request.user
    vehicles = Vehicle.objects.filter(user=user)
    if request.method == "POST" and 'vehicle_uuid' in request.POST:
        vehicle_uuid = request.POST['vehicle_uuid']
        vehicle = get_object_or_404(Vehicle, pk=vehicle_uuid)
        vehicle.delete()
        return redirect('display_vehicles')

    return render(request, 'display_vehicles.html', {'vehicles': vehicles})


def vehicle_details(request, vehicle_uuid):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_uuid)
    try:
        vehicle_booking = Booking.objects.get(vehicle=vehicle_uuid)
    except Booking.DoesNotExist:
        vehicle_booking = None
    context = {
        'vehicle': vehicle,
        'vehicle_booking': vehicle_booking
    }

    return render(request, 'vehicle_details.html', context)


def edit_vehicle_view(request, vehicle_uuid):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_uuid)
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            if 'image' in request.FILES:
                vehicle.image = form.cleaned_data['image']
            form.save()
            return redirect('vehicle_details', vehicle_uuid=vehicle_uuid)
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, 'edit-vehicle.html', {'form': form})


def vehicle_create_view(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            license_plate = form.cleaned_data['license_plate']
            if not Vehicle.objects.filter(license_plate=license_plate).exists():
                vehicle.save()
                return redirect('display_vehicles')
            else:
                messages.error(request, 'Vehicle with this License Plate already added')

    else:
        form = VehicleForm()
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
