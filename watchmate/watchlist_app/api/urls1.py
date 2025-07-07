
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import PlatformVS

router = DefaultRouter()
router.register('', PlatformVS, basename="platform")

urlpatterns = [
    path('', include(router.urls)),
]
