from django.urls import path
from .views import (
    SystemBTestView,
    UserPreferenceListCreateView,
    UserPreferenceDetailView,
)

urlpatterns = [
    path('test/', SystemBTestView.as_view(), name='system_b_test'),
    path('preferences/', UserPreferenceListCreateView.as_view(), name='preference-list-create'),
    path('preferences/<uuid:user_id>/', UserPreferenceDetailView.as_view(), name='preference-detail'),
]
