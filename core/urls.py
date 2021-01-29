from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), # Look in Home first
    # Otherwise, route to django auth stuff
    path('', include('django.contrib.auth.urls')),
    path('', include('accounts.urls')),

    # Third party stuff
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)