from .serializers import ScoreSerializer 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Score


class SubmitScoreView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        print('the request.data is', request.data)
        game = request.data.get('game')
        score = request.data.get('score')
        reward = request.data.get('reward')

        if not game or score < 0:
            return Response({'error': 'Game and score are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            score = int(score) 
        except ValueError:
            return Response({'error': 'Score must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # Check if a score entry already exists for the user and game
        existing_score = Score.objects.filter(user=user, game=game).first()

        if existing_score:
            existing_score.score += score
            existing_score.reward += reward
            existing_score.save()
            return Response({'message': 'Score updated successfully'}, status=status.HTTP_200_OK)
        else:
            # Create a new score entry
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({'message': 'Score submitted successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScoreListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def get_queryset(self):
        user = self.request.user
        return Score.objects.filter(user=user)


class ListAllScores(generics.ListAPIView):
    serializer_class = ScoreSerializer

    def get_queryset(self):
        game = self.request.query_params.get('game')
        if game:
            return Score.objects.filter(game=game)
        return Score.objects.all()
