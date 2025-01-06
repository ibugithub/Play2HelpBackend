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
from .models import MerkelDatastructure, Game, TokenInfo, Members, TotalScore, Brands
from datetime import date, timedelta
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta



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
  authentication_classes = [JWTAuthentication]

  def post(self, request):
    claimed_tokens = float(request.data.get('claimed_tokens'))
    last_claimed_date = request.data.get('last_claimed_date')
    game = request.data.get('game')
    gameModel = Game.objects.get(name=game)
    if not last_claimed_date:
      return Response({"error": "last claimed date is required"}, status=status.HTTP_400_BAD_REQUEST)
    if claimed_tokens is None:
      return Response({"error": "Claimed tokens are required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
      user = request.user
      scoreModel = Score.objects.get(user=user, game=gameModel)
      scoreModel.claimed_tokens += claimed_tokens
      scoreModel.last_claimed_date = last_claimed_date
      # the date format =>  "last_claimed_date": "2024-12-12T12:34:56Z"
      scoreModel.save()
      return Response({"message": "Tokens claimed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    def get(self, request, *args, **kwargs):
        try:
            allScores = Score.objects.all()
            scores_with_token_info = []

            if allScores.exists():
                for score in allScores:
                    try:
                        userWalletAddress = score.user.wallet_address
                        tokenAmount = score.tokens
                        tokenAddress = score.game.tokenInfo.bnb_contract_address
                        scores_with_token_info.append({
                            "userWalletAddress": userWalletAddress,
                            "tokenAmount": tokenAmount,
                            "tokenAddress": tokenAddress,
                        })
                    except AttributeError as attr_error:
                        print(f"Missing data for score ID {score.id}: {str(attr_error)}")
                print("Scores with token info:", scores_with_token_info)
            else:
                print("No scores found in the database.")

            return Response(scores_with_token_info, status=status.HTTP_200_OK)

        except Exception as e:
            print("An error occurred:", str(e))
            return Response({"error": "An error occurred while retrieving scores."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CalculateOwnership(APIView):
    def get(self, request, *args, **kwargs):
        defaultBrand = Brands.objects.filter(name="default").first()
        totalTokens = defaultBrand.total_tokens
        tokenPrices = defaultBrand.token_prices
        month = 0
        expiryDate = defaultBrand.token_count_date + timedelta(days=defaultBrand.token_duration) * 30
        today = date.today()
        if today > expiryDate:
            return Response({"error": "Token count date has expired"}, status=status.HTTP_400_BAD_REQUEST)
        timePassed = today - defaultBrand.token_count_date
        if timePassed.days <= 30:
            month = .5
        elif timePassed.days <= 60:
            month = .3
        else:
            month = .2
        
        members = Members.objects.all()
        for member in members:
            role = member.role
            if role == 'super_founder':
                superFounderCount = len(members.filter(role='super_founder'))
                member.ownership = round((totalTokens * tokenPrices * .20 * month) / superFounderCount, 3)
                member.save()
            elif role == 'super_builder':
                superBuilderCount = len(members.filter(role='super_builder'))
                member.ownership = round((totalTokens * tokenPrices * .35 * month) / superBuilderCount, 3)
                member.save()
            elif role == 'super_communicator':
                superCommunicatorCount = len(members.filter(role='super_communicator'))
                member.ownership = round((totalTokens * tokenPrices * .25 * month) / superCommunicatorCount, 3)
                member.save()
            elif role == 'founder':
                founderCount = len(members.filter(role='founder'))
                member.ownership = round((totalTokens * tokenPrices * .05 * month) / founderCount, 3)
                member.save()
            elif role == 'builder':
                builderCount = len(members.filter(role='builder'))
                member.ownership = round((totalTokens * tokenPrices * .05 * month) / builderCount, 3)
                member.save()
            elif role == 'communicator':
                communicatorCount = len(members.filter(role='communicator'))
                member.ownership = round((totalTokens * tokenPrices * .05 * month) / communicatorCount, 3)
                member.save()
            elif role == 'tourist':
                touristCount = len(members.filter(role='tourist'))
                member.ownership = round((totalTokens * tokenPrices * .035 * month) / touristCount, 3)
                member.save()
            elif role == 'listener':
                listenerCount = len(members.filter(role='listener'))
                member.ownership = round((totalTokens * tokenPrices * .015 * month) / listenerCount, 3)
                member.save()
        return Response({"ownership has been set successfully"}, status=status.HTTP_200_OK)