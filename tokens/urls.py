from django.urls import path
from .views import MerkelDataView, GetMerkelDataView, GetTokenInfoView

urlpatterns = [
  path('setMerkelDatastructure/', MerkelDataView.as_view(), name='merkel_datastructure'),
  path('getMerkelDataView/', GetMerkelDataView.as_view(), name='getMerkelDataView'),
  path('getTokenInfo/', GetTokenInfoView.as_view(), name='get_token_info')
]