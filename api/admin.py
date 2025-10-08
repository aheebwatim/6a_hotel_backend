from django.contrib import admin
from django.utils.html import format_html
from .models import Room, Reservation


# ============================================================
# ROOM ADMIN
# ============================================================
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "price_per_night", "availability_status")
    list_filter = ("is_available",)
    search_fields = ("name", "description",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    def availability_status(self, obj):
        color = "green" if obj.is_available else "red"
        text = "Available" if obj.is_available else "Occupied"
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>', color, text
        )
    availability_status.short_description = "Availability"


# ============================================================
# RESERVATION ADMIN
# ============================================================
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "colored_status",
        "confirmation_code",
        "room",
        "guest_name",
        "check_in",
        "check_out",
        "created_at",
    )
    list_filter = (
        "status",
        "room",
        ("check_in", admin.DateFieldListFilter),
    )
    search_fields = (
        "confirmation_code",
        "guest_name",
        "guest_email",
        "guest_phone",
        "room__name",
    )
    readonly_fields = ("confirmation_code", "created_at", "updated_at")
    date_hierarchy = "check_in"
    ordering = ("-created_at",)

    fieldsets = (
        ("Guest Information", {
            "fields": (
                "guest_name",
                "guest_email",
                "guest_phone",
                "num_guests",
            ),
        }),
        ("Reservation Details", {
            "fields": (
                "room",
                "check_in",
                "check_out",
                "special_requests",
                "status",
                "confirmation_code",
            ),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    def colored_status(self, obj):
        color_map = {
            "PENDING": "#c47f00",
            "CONFIRMED": "#0f8a00",
            "CANCELLED": "#b80000",
        }
        color = color_map.get(obj.status, "gray")
        return format_html(
            '<b><span style="color:{};">{}</span></b>', color, obj.get_status_display()
        )
    colored_status.short_description = "Status"
