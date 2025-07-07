from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Watchlist and Reviews API
    path('api/watchlist/', include('watchlist_app.api.urls')),

    # Platform (streaming service) API using routers
    path('api/platforms/', include('watchlist_app.api.urls1')),

    # User Account API
    path('api/account/', include('account_app.api.urls')),

    # path('api-auth/', include('rest_framework.urls')),
]
