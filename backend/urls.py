from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve
from django.views.generic import TemplateView
import os
from backend.settings import BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scanner.urls')),
    # Add catch-all route for React app
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^(manifest\.json|favicon\.ico|logo192\.png|logo512\.png)$', static_serve, {
        'document_root': os.path.join(BASE_DIR, 'nmapscanner/build'),
    }),
]