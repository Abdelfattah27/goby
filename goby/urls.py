from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from .auth_views import CustomAsyncTokenObtainPairView, CustomAsyncTokenRefreshView
from users.views import get_authenticated_user

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views
urlpatterns = [
    path("",views.landing ,name="landing"),
    path("for-restaurants/",views.for_restaurants ,name="for-restaurants"),
    path("privacy-policy/",views.privacy_policy ,name="privacy-policy"),
    path("terms-of-service/",views.terms_of_service ,name="terms-of-service"),
    path("auth/",views.login ,name="login-signup"),
    path("admin/", admin.site.urls),
    # path('api/gym-data/', include('gym_data.urls')),
    path("api/users/", include("users.urls")),
    path(
        "api/get_authenticated_user/",
        get_authenticated_user,
        name="get-authenticated-user",
    ),
    # path('api/subscriptions/', include('subscriptions.urls')),
    # path('api/financials/', include('financials.urls')),
    path("api/clients/", include("clients.urls")),
    path("api/restaurants/", include("restaurants.urls")),
    path("api/delivery/", include("delivery.urls")),
    # path('api/shop/', include('shop.urls')),
    # path('api/reports/', include('reports.urls')),
    path("token/", CustomAsyncTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomAsyncTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
    path("auth/", include("authentication.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
