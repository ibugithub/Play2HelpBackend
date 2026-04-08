from django.test import TestCase
from rest_framework.test import APIClient

from games.models import FrontendSite, Game, Score, TotalScore
from tokens.models import TokenInfo
from users.models import User


class SubmitScoreViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="player@example.com",
            name="Player One",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)
        self.token_info = TokenInfo.objects.create(
            token_name="Test Token",
            token_symbol="TT",
            bnb_contract_address="0x123",
            solana_contract_address="So11111111111111111111111111111111111111112",
            total_value=1000000,
            token_prices=1.0,
        )
        self.game = Game.objects.create(name="Math Run", tokenInfo=self.token_info)

    def test_submit_score_tracks_frontend_site_separately(self):
        payload = {
            "game": self.game.name,
            "score": 10,
            "tokens": 1.5,
            "source_site": "weplay2help",
        }
        response = self.client.post("/games/submitScore/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        payload["source_site"] = "weplay2learn"
        response = self.client.post("/games/submitScore/", payload, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Score.objects.count(), 2)
        self.assertTrue(Score.objects.filter(source_site=FrontendSite.WEPLAY2HELP, game=self.game, user=self.user).exists())
        self.assertTrue(Score.objects.filter(source_site=FrontendSite.WEPLAY2LEARN, game=self.game, user=self.user).exists())

        total_score = TotalScore.objects.get(user=self.user)
        self.assertEqual(total_score.total_score, 20)
        self.assertEqual(total_score.total_tokens, 3.0)

    def test_submit_score_accepts_weplah2help_alias(self):
        payload = {
            "game": self.game.name,
            "score": 5,
            "tokens": 2,
            "source_site": "weplah2help",
        }
        response = self.client.post("/games/submitScore/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Score.objects.filter(source_site=FrontendSite.WEPLAY2HELP).exists())
