from django.urls import path
from .views import TelemetryView, IncidentList, ScanSnippetView, RemediateView

urlpatterns = [
    path('telemetry/', TelemetryView.as_view(), name='telemetry'),
    path('incidents/', IncidentList.as_view(), name='incidents'),
    path('scan-snippet/', ScanSnippetView.as_view(), name='scan_snippet'),
    path('remediate/', RemediateView.as_view(), name='remediate'),
]