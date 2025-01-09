from .serializers import MerkelDatastructureSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.response import Response
from .models import MerkelDatastructure


class MerkelDataView(APIView):
    def post(self, request):
        serializer = MerkelDatastructureSerializer(data=request.data)
        
        if serializer.is_valid():
            instance, created = MerkelDatastructure.objects.update_or_create(
                id=MerkelDatastructure.objects.first().id if MerkelDatastructure.objects.exists() else None,
                defaults=serializer.validated_data
            )
            
            return Response(
                {"message": "Data saved successfully", "data": MerkelDatastructureSerializer(instance).data},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class GetMerkelDataView(APIView):
    def get(self, request):
        """
        Get the single MerkelDatastructure entry.
        """
        try:
            merkel_data = MerkelDatastructure.objects.first()
            if not merkel_data:
                return Response(
                    {"error": "No data found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = MerkelDatastructureSerializer(merkel_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
