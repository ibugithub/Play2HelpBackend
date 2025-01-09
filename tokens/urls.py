from django.urls import path
from .views import MerkelDataView, GetMerkelDataView

urlpatterns = [
  path('setMerkelDatastructure/', MerkelDataView.as_view(), name='merkel_datastructure'),
  path('getMerkelDataView/', GetMerkelDataView.as_view(), name='getMerkelDataView'),
]