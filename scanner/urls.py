from django.urls import path
from django.views.generic import TemplateView
from .views import ContactFormView, RegisterView, LoginView, ScanView, ScanResultView

urlpatterns = [
    # Frontend SPA routes (React handles routing internally)
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='index.html'), name='about'),
    path('result/', TemplateView.as_view(template_name='index.html'), name='result'),
    path('documentation/', TemplateView.as_view(template_name='index.html'), name='documentation'),
    path('contact/', TemplateView.as_view(template_name='index.html'), name='contact'),
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
    # Changed frontend signup route to avoid conflict
    path('signup-page/', TemplateView.as_view(template_name='index.html'), name='signup'),

    # ✅ API routes (avoid collision with frontend)
    path('api/contact/', ContactFormView.as_view(), name='contact-form'),
    path('api/signup/', RegisterView.as_view(), name='signup-api'),  # API endpoint for signup
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/scan/', ScanView.as_view(), name='scan'),  # Updated to ScanView
    path('api/scan-result/<int:scan_id>/', ScanResultView.as_view(), name='scan-result'),
]
