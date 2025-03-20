from django.urls import path
from .views import (
    SystemATestView,
    UserProfileListCreateView,
    UserProfileDetailView,
    DepartmentListCreateView,
    DepartmentDetailView,
)

urlpatterns = [
    path('test/', SystemATestView.as_view(), name='system_a_test'),
    path('profiles/', UserProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<uuid:user_id>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
]
