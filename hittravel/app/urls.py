from django.urls import path
from .views import TourListCreateView, TourRequestListCreateView, TourRequestDetailView

urlpatterns = [
    path('tours/', TourListCreateView.as_view(), name='tour-list-create'),
    path('tour-requests/', TourRequestListCreateView.as_view(), name='tour-request-list-create'),
    path('tour-requests/<int:pk>/', TourRequestDetailView.as_view(), name='tour-request-detail'),
]