from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid


# ============================================================
# ROOM MODEL
# ============================================================
class Room(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    capacity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="rooms/", blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Cap: {self.capacity})"


# ============================================================
# RESERVATION MODEL
# ============================================================
class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    guest_name = models.CharField(max_length=120, default="Guest")
    guest_email = models.EmailField(default="default@example.com")
    guest_phone = models.CharField(max_length=30, default="+0000000000")
    num_guests = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField(default=timezone.now)
    special_requests = models.TextField(blank=True)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )
    confirmation_code = models.CharField(
        max_length=36, unique=True, editable=False, default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out__gt=models.F("check_in")),
                name="check_out_after_check_in",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def overlaps(self, other_start, other_end):
        # Overlap if existing.start < new.end AND existing.end > new.start
        return (
            self.check_in < other_end
            and self.check_out > other_start
        )

    def __str__(self):
        return f"{self.room.name} • {self.guest_name} • {self.check_in}→{self.check_out}"
