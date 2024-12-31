from .serializers import ScoreSerializer, TokenInfoSerializer, MemberSerializer, TotalScoreSerializer, MerkelDatastructureSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .models import Score, User
from django.utils.dateparse import parse_datetime
from rest_framework import generics, permissions
from .models import MerkelDatastructure, Game, TokenInfo, Members, TotalScore

class SubmitScoreView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        print('the request.data is', request.data)
        gameName = request.data.get('game')
        game = Game.objects.filter(name=gameName).first()
        score = request.data.get('score')
        tokens = request.data.get('tokens')
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
        existing_score = Score.objects.filter(user=user, game=game.id).first()
        existing_total_score = TotalScore.objects.filter(user=user).first()

        if existing_score:
            existing_score.score += score
            existing_score.tokens += tokens
            existing_score.save()
            score_response = {'message': 'Score updated successfully'}
        else:
            # Create a new score entry
            if serializer.is_valid():
                serializer.save(user=user, game=game)
                score_response = {'message': 'Score submitted successfully'}
            else:
                print('the serializer error is', serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if existing_total_score:
            existing_total_score.total_score += score
            existing_total_score.total_tokens += tokens
            existing_total_score.save()
        else:
            TotalScore.objects.create(user=user, total_score=score, total_tokens=tokens)
            
        return Response({**score_response}, status=status.HTTP_200_OK)

class ScoreListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def get_queryset(self):
        user = self.request.user
        return Score.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        user = request.user
        print('the response.data is', response.data)
        response.data = {
            'scores': response.data
        }
        return response

class ListAllScores(generics.ListAPIView): 
    serializer_class = ScoreSerializer

    def get_queryset(self):
        gameName = self.request.query_params.get('game')
        game = Game.objects.filter(name=gameName).first()
        if game:
            return Score.objects.filter(game=game).order_by('-score')
        return Score.objects.all().order_by('-score')

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
      scoreModel = Score.objects.get(user=user)
      scoreModel.claimed_tokens += claimed_tokens
      scoreModel.total_tokens -= claimed_tokens
      scoreModel.last_claimed_date = last_claimed_date
      # the date format =>  "last_claimed_date": "2024-12-12T12:34:56Z"
      scoreModel.save()
      return Response({"message": "Tokens claimed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MerkelDataView(APIView):
    def post(self, request):
        serializer = MerkelDatastructureSerializer(data=request.data)

        # Validate the data using the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Data saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
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

class GetScoreDataView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    gameName = request.GET.get('gameName')
    try:
      game = Game.objects.get(name=gameName)
      tokenInfo = TokenInfo.objects.get(id=game.tokenInfo.id)
      serializer = TokenInfoSerializer(tokenInfo)
      return Response({
        "tokenInfo": serializer.data,
      }, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)   

class GetTotalScoresView(APIView):
    def get(self, request):
        try:
            total_scores = TotalScore.objects.all().order_by('-total_score')
            serializer = TotalScoreSerializer(total_scores, many=True)
            return Response({
                "total_scores": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getMemberData(APIView):
    def get(self, request):
        try:
            member = Members.objects.all()
            serializer = MemberSerializer(member, many=True)
            return Response({
                "member": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
class GetAllScoresWithTokenInfo(APIView):
    print('The GetAllScores view is initialized')

    def get(self, request, *args, **kwargs):
        try:
            allScores = Score.objects.all()
            if allScores:
                print('First score is', allScores[0].game.tokenInfo.bnb_contract_address)
                print('the token amount is', allScores[0].tokens)
            else:
                print('No scores found in the database.')
            
            serializer = ScoreSerializer(allScores, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print('An error occurred:', str(e))
            return Response({"error": "An error occurred while retrieving scores."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    