from rest_framework import generics
from .models import Ad
from .serializers import AdSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import World
from .serializers import WorldSerializer
from django.shortcuts import render, get_object_or_404


# List all ads or create a new one
class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

# Retrieve, update, or delete a specific ad
class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

def get_categories(request):
    # Get distinct categories from the Ad model
    categories = Ad.objects.values_list('category', flat=True).distinct()
    return JsonResponse({"categories": list(categories)})


class WorldView(APIView):
    def get(self, request):
        worlds = World.objects.all()
        serializer = WorldSerializer(worlds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List of worlds
class AdsForWorldView(APIView):
    def get(self, request, world_name):
        try:
            # Fetch the world object
            world = World.objects.get(name=world_name)

            # Get ads that match the categories of the world
            ads = Ad.objects.filter(category__in=world.ad_categories)

            # Serialize the ads
            serializer = AdSerializer(ads, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except World.DoesNotExist:
            return Response({"error": f"World '{world_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

# Server-side ad preview
class AdsPreview(APIView):
    def get(self, request, world_name, ad_number=None):
        try:
            # Fetch the world object
            world = get_object_or_404(World, name=world_name)

            # Filter ads by the world's categories
            ads = Ad.objects.filter(category__in=world.ad_categories)

            if ad_number is None:
                # Return the serialized list of ads for the world
                serializer = AdSerializer(ads, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Render a specific ad
            try:
                ad = ads[int(ad_number) - 1]  # Adjust for 0-based index
            except IndexError:
                return Response(
                    {"error": f"No ad found for world '{world_name}' at position {ad_number}."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Render the template with the specific ad
            return render(request, "ad-render.html", {"ad": ad, "world": world})

        except World.DoesNotExist:
            return Response(
                {"error": f"World '{world_name}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )