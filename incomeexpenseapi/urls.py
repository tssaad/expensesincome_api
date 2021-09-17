
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="INCOME EXPENESE API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.test.com/policies/terms/",
      contact=openapi.Contact(email="test@test.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('expenses/', include('expenses.urls')),
    path('income/', include('income.urls')),
    path('userstat/', include('userstat.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-without-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


handler404='utils.views.error_404'
handler500='utils.views.error_500'