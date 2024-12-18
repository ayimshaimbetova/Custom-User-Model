from django.contrib import admin
from django.urls import path, include 
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title = 'News',
        description = 'documentation',
        default_version = 'v1',
    ),
    public = True
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("articles/", include("articles.urls")), 
    path("api/", include("api.urls")),
    path("", include("pages.urls")), 
    path("api-auth/", include("rest_framework.urls")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")), 
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
