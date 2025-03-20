from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from auth_service.views import RegisterView, LoginView, UserProfileView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django SSO API",
        default_version='v1',
        description="""
        API documentation for Django SSO Project.
        
        This API provides endpoints for:
        * User Authentication (PostgreSQL)
        * User Profiles (MySQL)
        * User Preferences (MongoDB)
        * Department Management
        """,
        terms_of_service="https://shabeehnaqvi.com",
        contact=openapi.Contact(email="s.naqvi2129@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
    patterns=[
        path('api/', include([
            path('register/', RegisterView.as_view()),
            path('login/', LoginView.as_view()),
            path('profile/', UserProfileView.as_view()),
            path('system-a/', include('system_a.urls')),
            path('system-b/', include('system_b.urls')),
        ])),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/system-a/', include('system_a.urls')),
    path('api/system-b/', include('system_b.urls')),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
