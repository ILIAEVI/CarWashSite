from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class CreateVehicle(models.Model):

    class BodyShapeChoices(models.TextChoices):
        SUV = "suv", _("S-U-V")
        SEDAN = "sedan", _("Sedan")
        SMALL_CAR = "small_car", _("Small Car or Convertible")
        VAN_MINIBUS = "van_minibus", _("VAN/Minibus")
        TRANSPORTER = "transporter", _("Transporter")

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    brand = models.CharField(max_length=255, help_text=_("Enter Brand name"))
    body_shape = models.CharField(
        max_length=255,
        choices=BodyShapeChoices.choices,
        default=BodyShapeChoices.SEDAN,
        help_text=_("Choice your car's body shape")

    )
    model = models.CharField(max_length=255, help_text=_("Enter your car's model"))
    license_plate = models.CharField(max_length=7, help_text=_("Enter your car's license plate. EX:(HQ327QH)"))

    def __str__(self):
        return "Brand: " + self.brand + " | License: " + self.license_plate


class Booking(models.Model):
    class CarWashServiceChoices(models.TextChoices):
        FULL_CLEAN = "full_clean", _("Full Service:(Included Detailing)")
        DETAILING = "detailing", _("Detailing")
        ENGINE_CLEAN = "engine_clean", _("Engine Depressing & Coating")
        AC_TREATMENT = "ac_treatment", _("A.C. Treatment")
        INTERNAL_LEANING = "internal_cleaning", _("Intensive internal cleaning(dry)")
        BODY_WASH = "body_wash", _("Body Shampooing and Washing")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(CreateVehicle, on_delete=models.CASCADE)
    service = models.CharField(
        max_length=255,
        choices=CarWashServiceChoices.choices,
        default=CarWashServiceChoices.BODY_WASH,
        help_text=_("Choice Service")

    )
    datetime = models.DateTimeField(help_text=_("Choose the date and time of your visit"))
