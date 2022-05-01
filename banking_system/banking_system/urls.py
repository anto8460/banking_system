from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('banking_system_app.urls')),
    path('login/', include('login_app.urls')),
    path('login/', include('login_app.urls')),
    path('admin/', admin.site.urls),
]
