from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

API_VERSION = "v1"


def get_api_path(path):
    return r"^api/(?P<version>({}))/{}".format(API_VERSION, path)


class CustomDefaultRouter(routers.DefaultRouter):
    include_root_view = not settings.IS_SERVER_SECURE


router = CustomDefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    # DRF router
    re_path(get_api_path(""), include(router.urls)),
    # JWT
    re_path(
        get_api_path(r"jwt/create/$"), TokenObtainPairView.as_view(), name="jwt-create"
    ),
    re_path(
        get_api_path(r"jwt/refresh/$"), TokenRefreshView.as_view(), name="jwt-refresh"
    ),
    re_path(
        get_api_path(r"jwt/verify/$"), TokenVerifyView.as_view(), name="jwt-verify"
    ),
    # DRF spectaular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]

if not settings.IS_SERVER_SECURE:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]