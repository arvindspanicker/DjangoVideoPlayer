# Django imports
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('videos.urls')),
    path('jet', include('jet.urls', 'jet')),  # Django JET URLS
    path('secure_admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]


 # Only used in Debugging mode
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
