from django.urls import path
from .views import SystemBTestView

urlpatterns = [
    path('test/', SystemBTestView.as_view(), name='system_b_test'),
]
