from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from HQapp.views import AccessibleProductsListView


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="API documentation",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="bar.norilsk@gmail.com"),
      license=openapi.License(name="alpha"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('HQapp.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

