from watchlist_app.api.views import (
    WatchlistAV, WatchlistDetailAV,
    ReviewlistAV, ReviewDetailAV, 
    ReviewCreateAV, Reviewlistbyuser
)
from django.urls import path

urlpatterns = [
    path('', WatchlistAV.as_view(), name="watchlist-list-create"),
    path('<int:pk>/', WatchlistDetailAV.as_view(), name="watchlist-detail"),
    path('<int:pk>/reviews/', ReviewlistAV.as_view(), name="watchlist-review-list"),
    path('<int:pk>/review/', ReviewCreateAV.as_view(), name="watchlist-review-create"),

    path('reviews/<int:pk>/', ReviewDetailAV.as_view(), name="review-detail"),      
    path('reviews/by-user/', Reviewlistbyuser.as_view(), name="review-by-user"),
]
