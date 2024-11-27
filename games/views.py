from django.shortcuts import render
from .models import Score
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
    if serializer.is_valid():
      user = request.user
      print('the user is:', user)
      score = serializer.validated_data['score']
      # Score.objects.create(user=user, score=score)
      serializer.save(user=request.user)
      return Response({'message': 'Score submitted successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)