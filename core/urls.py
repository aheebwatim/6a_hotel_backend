from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),  # adds /api/contact/
]
                    
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/auth/", include("api.jwt_urls")),
    path("hotel/", include("hotel.urls")),

    # React frontend catch-all
    re_path(r"^.*$", TemplateView.as_view(template_name="index.html")),
]
