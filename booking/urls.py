from django.urls import path
from . import views

urlpatterns = [
    path("addvehicle/", views.vehicle_create_view, name='add_vehicle'),
    path("bookvisit/", views.book_visit_view, name='book_visit'),
]
