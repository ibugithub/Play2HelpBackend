from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from members.models import Members
from members.serializers import MemberSerializer
from tokens.models import TokenInfo
from tokens.serializers import TokenInfoSerializer

from .models import FrontendSite, Game, Score, TotalScore
from .serializers import ScoreSerializer, TotalScoreSerializer


FRONTEND_SITE_ALIASES = {
    "weplah2help": FrontendSite.WEPLAY2HELP,
    "weplay2help": FrontendSite.WEPLAY2HELP,
    "weplay2health": FrontendSite.WEPLAY2HEALTH,
    "weplay2learn": FrontendSite.WEPLAY2LEARN,
    "weplay2love": FrontendSite.WEPLAY2LOVE,
    "weplay2work": FrontendSite.WEPLAY2WORK,
}


def normalize_frontend_site(value):
    if value is None:
        return FrontendSite.UNKNOWN
    return FRONTEND_SITE_ALIASES.get(str(value).strip().lower())


class SubmitScoreView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        print("the request.data is", request.data)

        game_name = request.data.get("game")
        source_site = normalize_frontend_site(request.data.get("source_site"))
        game = Game.objects.filter(name=game_name).first()
        score = request.data.get("score")
        tokens = request.data.get("tokens")

        if not source_site:
            return Response(
                {
                    "error": "source_site is invalid.",
                    "allowed_sites": [choice for choice, _ in FrontendSite.choices if choice != FrontendSite.UNKNOWN],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tokens = float(tokens)
        except (TypeError, ValueError):
            return Response({"error": "Tokens must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            score = int(score)
        except (TypeError, ValueError):
            return Response({"error": "Score must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if not game_name or score < 0:
            return Response({"error": "Game is a required field."}, status=status.HTTP_400_BAD_REQUEST)

        if not game:
            return Response({"error": "Game not found in the db."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        existing_score = Score.objects.filter(user=user, game=game, source_site=source_site).first()
        existing_total_score = TotalScore.objects.filter(user=user).first()

        if existing_score:
            existing_score.score += score
            existing_score.tokens += tokens
            existing_score.save()
            score_response = {"message": "Score updated successfully"}
        else:
            if serializer.is_valid():
                serializer.save(user=user, game=game, source_site=source_site)
                score_response = {"message": "Score submitted successfully"}
            else:
                print("the serializer error is", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if existing_total_score:
            existing_total_score.total_score += score
            existing_total_score.total_tokens += tokens
            existing_total_score.save()
        else:
            TotalScore.objects.create(user=user, total_score=score, total_tokens=tokens)

        return Response(score_response, status=status.HTTP_200_OK)


class ScoreListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def get_queryset(self):
        user = self.request.user
        source_site = normalize_frontend_site(self.request.query_params.get("source_site"))
        queryset = Score.objects.filter(user=user)
        if source_site:
            queryset = queryset.filter(source_site=source_site)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            "scores": response.data
        }
        return response


class ListAllScores(generics.ListAPIView):
    serializer_class = ScoreSerializer

    def get_queryset(self):
        game_name = self.request.query_params.get("game")
        source_site = normalize_frontend_site(self.request.query_params.get("source_site"))
        game = Game.objects.filter(name=game_name).first()
        queryset = Score.objects.all()
        if game:
            queryset = queryset.filter(game=game)
        if source_site:
            queryset = queryset.filter(source_site=source_site)
        return queryset.order_by("-score")


class SetClaimTokensView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        claimed_tokens = float(request.data.get("claimed_tokens"))
        last_claimed_date = request.data.get("last_claimed_date")
        game = request.data.get("game")
        source_site = normalize_frontend_site(request.data.get("source_site"))
        game_model = Game.objects.get(name=game)
        if not last_claimed_date:
            return Response({"error": "last claimed date is required"}, status=status.HTTP_400_BAD_REQUEST)
        if claimed_tokens is None:
            return Response({"error": "Claimed tokens are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = request.user
            score_queryset = Score.objects.filter(user=user, game=game_model)
            if source_site:
                score_queryset = score_queryset.filter(source_site=source_site)
            if score_queryset.count() > 1:
                return Response(
                    {"error": "Multiple score rows found for this game. Please provide source_site."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            score_model = score_queryset.get()
            score_model.claimed_tokens += claimed_tokens
            score_model.last_claimed_date = last_claimed_date
            score_model.save()
            return Response({"message": "Tokens claimed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetScoreDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        game_name = request.GET.get("gameName")
        try:
            game = Game.objects.get(name=game_name)
            token_info = TokenInfo.objects.get(id=game.tokenInfo.id)
            serializer = TokenInfoSerializer(token_info)
            return Response({
                "tokenInfo": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetTotalScoresView(APIView):
    def get(self, request):
        try:
            total_scores = TotalScore.objects.all().order_by("-total_score")
            serializer = TotalScoreSerializer(total_scores, many=True)
            return Response({
                "total_scores": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetMembersView(APIView):
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
            all_scores = Score.objects.all()
            scores_with_token_info = []

            if all_scores.exists():
                for score in all_scores:
                    try:
                        user_wallet_address = score.user.wallet_address
                        token_amount = score.tokens
                        token_address = score.game.tokenInfo.bnb_contract_address
                        scores_with_token_info.append({
                            "userWalletAddress": user_wallet_address,
                            "tokenAmount": token_amount,
                            "tokenAddress": token_address,
                            "sourceSite": score.source_site,
                            "game": score.game.name,
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
