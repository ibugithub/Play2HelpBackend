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
    def get(self, request, world_name, index=None):
        try:
            # Fetch the world object
            world = World.objects.get(name=world_name)

            # Get ads that match the categories of the world
            ads = Ad.objects.filter(category__in=world.ad_categories)

            # If an index is provided, fetch only the specific ad
            if index is not None:
                try:
                    ad = ads[int(index)]  # Get the ad at the given index
                    serializer = AdSerializer(ad)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except IndexError:
                    return Response(
                        {"error": f"No ad found at index {index}."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                # Serialize all ads if no index is provided
                serializer = AdSerializer(ads, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except World.DoesNotExist:
            return Response(
                {"error": f"World '{world_name}' does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


# Server-side ad preview
class AdsPreview(APIView):
    def get(self, request, world_name, ad_number=None):
        # Get the specified world or return a 404 error
        world = get_object_or_404(World, name=world_name)

        # Get ads that belong to the world's categories
        ads = Ad.objects.filter(category__in=world.ad_categories).order_by('id')  # Order ads explicitly

        if not ads.exists():
            return Response(
                {"error": f"No ads found for the world '{world_name}'."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Render a specific ad based on the ad_number
        try:
            ad_number = int(ad_number)  # Ensure ad_number is an integer
            ad = ads[ad_number - 1]  # Adjust to 0-based index for the queryset
        except (ValueError, IndexError):
            return Response(
                {"error": f"Invalid ad number '{ad_number}' for the world '{world_name}'."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Render the ad in the template
        return render(request, "ad-render.html", {"ad": ad, "world": world})