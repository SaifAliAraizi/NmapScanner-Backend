from django.urls import path
from django.views.generic import TemplateView
from .views import ContactFormView, RegisterView, LoginView, ScanView, ScanResultView

urlpatterns = [
    # API routes
    path('api/contact/', ContactFormView.as_view(), name='contact-form'),
    path('api/signup/', RegisterView.as_view(), name='signup-api'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/scan/', ScanView.as_view(), name='scan'),
    path('api/scan-result/<int:scan_id>/', ScanResultView.as_view(), name='scan-result'),
    
    # Frontend routes - let React handle these
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='index.html'), name='about'),
    path('result/', TemplateView.as_view(template_name='index.html'), name='result'),
    path('documentation/', TemplateView.as_view(template_name='index.html'), name='documentation'),
    path('contact/', TemplateView.as_view(template_name='index.html'), name='contact'),
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
    path('signup/', TemplateView.as_view(template_name='index.html'), name='signup'),
    path('scan/', TemplateView.as_view(template_name='index.html'), name='scan'),
]