from django.urls import path

from .views import VendorStatisticsAPIView, CustomerStatisticsAPIView


urlpatterns = [
    path("employee/<int:pk>/", VendorStatisticsAPIView.as_view()),
    path("client/<int:pk>/", CustomerStatisticsAPIView.as_view()),
]
