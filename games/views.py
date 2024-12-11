from .serializers import ScoreSerializer ,TokensSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Score, Tokens


class SubmitScoreView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        print('the request.data is', request.data)
        game = request.data.get('game')
        score = request.data.get('score')
        tokens = request.data.get('tokens')

        if not game or int(score) < 0:
            return Response({'error': 'Game and score are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            score = int(score) 
        except ValueError:
            return Response({'error': 'Score must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # Check if a score entry already exists for the user and game
        existing_score = Score.objects.filter(user=user, game=game).first()
        existing_tokens = Tokens.objects.filter(user=user).first()

        if existing_score:
            existing_score.score += score
            existing_score.tokens += tokens
            existing_score.save()
            score_response = {'message': 'Score updated successfully'}
        else:
            # Create a new score entry
            if serializer.is_valid():
                serializer.save(user=user)
                score_response = {'message': 'Score submitted successfully'}
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if existing_tokens:
            existing_tokens.total_tokens += tokens
            existing_tokens.save()
            tokens_response = {'message': 'Tokens updated successfully'}
        else:
            # Create a new tokens entry
            serializer = TokensSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                tokens_response = {'message': 'Tokens submitted successfully'}
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({**score_response, **tokens_response}, status=status.HTTP_200_OK)

class ScoreListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def get_queryset(self):
        user = self.request.user
        print('the score obj is', Score.objects.filter(user=user))
        return Score.objects.filter(user=user)


class ListAllScores(generics.ListAPIView):
    serializer_class = ScoreSerializer

    def get_queryset(self):
        game = self.request.query_params.get('game')
        if game:
            print('the score obj is', Score.objects.filter(game=game))
            return Score.objects.filter(game=game)
        return Score.objects.all()
