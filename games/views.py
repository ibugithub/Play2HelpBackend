from .serializers import ScoreSerializer ,TokensSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Score, Tokens, User
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.dateparse import parse_datetime
from rest_framework import generics, permissions
from .models import MerkelDatastructure


class SubmitScoreView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        print('the request.data is', request.data)
        game = request.data.get('game')
        score = request.data.get('score')
        tokens = request.data.get('tokens')
        print('the single token is', tokens)
        try:
            tokens = float(tokens)
        except ValueError:
            return Response({'error': 'Tokens must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

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
            print('the token in existing score is', existing_score.tokens)
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
                new_tokens = serializer.save(user=user)
                new_tokens.total_tokens = tokens 
                new_tokens.save()
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

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        user = request.user
        tokens = Tokens.objects.filter(user=user).first()
        response.data = {
            'scores': response.data,
            'total_tokens': tokens.total_tokens if tokens else 0
        }
        return response


class ListAllScores(generics.ListAPIView):
    serializer_class = ScoreSerializer

    def get_queryset(self):
        game = self.request.query_params.get('game')
        if game:
            print('the score obj is', Score.objects.filter(game=game))
            return Score.objects.filter(game=game)
        return Score.objects.all()


class SetClaimTokensView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
      return Response({"error": "Invalid token header"}, status=status.HTTP_400_BAD_REQUEST)
    token = auth_header.split(' ')[1]
    claimed_tokens = request.data.get('claimed_tokens')
    last_claimed_date = request.data.get('last_claimed_date')
    if not last_claimed_date:
      return Response({"error": "last claimed date is required"}, status=status.HTTP_400_BAD_REQUEST)
    if claimed_tokens is None:
      return Response({"error": "Claimed tokens are required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
      access_token = AccessToken(token)
      user = User.objects.get(id=access_token['user_id'])
      tokensModel = Tokens.objects.get(user=user)
      tokensModel.claimed_tokens += claimed_tokens
      tokensModel.total_tokens -= claimed_tokens
      tokensModel.last_claimed_date = last_claimed_date
      # the date format =>  "last_claimed_date": "2024-12-12T12:34:56Z"
      tokensModel.save()
      return Response({"message": "Tokens claimed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class MerkelDataView(APIView):
    def post(self, request):
        serialized_leaves = request.data.get('serialized_leaves')
        modified_date = request.data.get('modified_date')

        # Validate the input data
        if not serialized_leaves or not modified_date:
            return Response(
                {"error": "Both 'serializedLeaves' and 'modifiedDate' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Parse modified_date to ensure it's in a valid datetime format
            parsed_modified_date = parse_datetime(modified_date)
            if not parsed_modified_date:
                return Response(
                    {"error": "Invalid date format for 'modifiedDate'. Use ISO 8601 format."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            merkel_data = MerkelDatastructure.objects.create(
                serialized_leaves=serialized_leaves,
                modified_date=parsed_modified_date
            )

            return Response(
                {"message": "Data saved successfully", "id": merkel_data.id},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
