from django.urls import path

# from admin.views import CRAdminFacultyAPIView, CRAdminUniversityAPIView
from .views import RegistrationApiView, LoginAPIView, LogoutView, VendorsStatisticsAPIView

urlpatterns = [
    path('register/', RegistrationApiView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('statistics/', VendorsStatisticsAPIView.as_view()),

]
