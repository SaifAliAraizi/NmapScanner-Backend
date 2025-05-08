from django.urls import path
from .views import ContactFormView, RegisterView, LoginView, ScanView, ScanResultView

urlpatterns = [
    # API routes only
    path('api/contact/', ContactFormView.as_view(), name='contact-form'),
    path('api/signup/', RegisterView.as_view(), name='signup-api'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/scan/', ScanView.as_view(), name='scan'),
    path('api/scan-result/<int:scan_id>/', ScanResultView.as_view(), name='scan-result'),
]
