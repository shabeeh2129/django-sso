from django.urls import path
from .views import SystemATestView

urlpatterns = [
    path('test/', SystemATestView.as_view(), name='system_a_test'),
]
