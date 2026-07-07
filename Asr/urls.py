from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_info = openapi.Info(
    title="API",
    default_version="v1",
    description="API",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    

    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
    ),
]

