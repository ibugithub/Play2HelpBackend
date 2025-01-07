from django.urls import path
from .views import AdListCreateView, AdDetailView, get_categories, WorldView, AdsForWorldView

urlpatterns = [
    path('ads/', AdListCreateView.as_view(), name='ad-list-create'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('ads/categories/', get_categories, name='get_categories'),
    path('worlds/', WorldView.as_view(), name='worlds'),
    path('worlds/<str:world_name>/ads/', AdsForWorldView.as_view(), name='ads_for_world'),
]
