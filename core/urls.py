from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/auth/", include("api.jwt_urls")),
    path("hotel/", include("hotel.urls")),

    # serve frontend only for non-admin, non-api routes
    re_path(r"^(?!admin|api|hotel).*", TemplateView.as_view(template_name="index.html")),
]
