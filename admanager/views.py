from rest_framework import generics
from .models import Ad
from .serializers import AdSerializer

# List all ads or create a new one
class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

# Retrieve, update, or delete a specific ad
class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
