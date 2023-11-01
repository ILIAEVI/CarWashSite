from django.urls import path
from . import views

urlpatterns = [
    path("addvehicle/", views.vehicle_create_view, name='add_vehicle'),
    path("bookvisit/", views.book_visit_view, name='book_visit'),
    path("vehicles/", views.display_all_vehicles, name='display_vehicles'),
    path('vehicle_details/<uuid:vehicle_uuid>/', views.vehicle_details, name='vehicle_details'),
    path('edit_vehicle/<uuid:vehicle_uuid>/', views.edit_vehicle_view, name='edit_vehicle'),
]

# path("delete-vehicle/", views.delete_vehicle, name='delete_vehicle'),
