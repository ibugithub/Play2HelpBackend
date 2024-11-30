from .serializers import ScoreSerializer 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class SubmitScoreView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = ScoreSerializer(data=request.data)
    print('the request.data is:', request.data)
    if serializer.is_valid():
      user = request.user
      print('the user is:', user)
      serializer.save(user=request.user)
      return Response({'message': 'Score submitted successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)