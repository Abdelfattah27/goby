from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
# router.register('employee', EmployeeViewSet, basename='employee')
# router.register('nationality', NationalityViewSet, basename='nationality')
# router.register('marital-status', MaritalStatusViewSet, basename='marital-status')
# router.register('employee-type', EmployeeTypeViewSet, basename='employee-type')
# router.register('city', CityViewSet, basename='city')
# router.register('city-district', CityDistrictViewSet, basename='city-district')
# router.register('moderator', ModeratorViewSet, basename='moderator')

urlpatterns = [
    path('', include(router.urls)),
    path('get_models_permissions/', get_models_permissions, name='get_models_permissions'),
    path('get_user_permissions/', get_user_permissions, name='get_user_permissions'),
    path('set_user_permissions/', set_user_permissions, name='set_user_permissions'),
]
