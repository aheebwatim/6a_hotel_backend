from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# ------------------------------
# Service Model
# ------------------------------
class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ------------------------------
# Reservation Model
# ------------------------------
class Reservation(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reservations")
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    reservation_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Prevent double booking for the same service at the same time
        if Reservation.objects.filter(
            service=self.service, reservation_date=self.reservation_date
        ).exists():
            raise ValidationError("This service is already booked at this time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest_name} - {self.service.name}"


# ------------------------------
# Room Model
# ------------------------------
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
