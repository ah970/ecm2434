"""Tests for game app."""

import datetime

from django.test import Client, TestCase
from django.contrib.auth.models import User

from .models import Player, Event, Participation, TreasureChest


class TestHTTPResponsesAndRedirectsNotLoggedIn(TestCase):
    """Class for testing HTTP responses and redirects when not logged in."""

    def test_response_home_view(self):
        """Test response for home view."""
        response = self.client.get("/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirect_game_views(self):
        """Test redirects for game related views."""
        # Game list view.
        response = self.client.get("/game/", follow=True)
        self.assertRedirects(response, "/login/?next=/game/")

        # Game view.
        response = self.client.get("/game/1/", follow=True)
        self.assertRedirects(response, "/login/?next=/game/1/")

        # Game over view.
        response = self.client.get("/game_over/", follow=True)
        self.assertEquals(response.status_code, 404)
        response = self.client.get("/game_over/1/", follow=True)
        self.assertRedirects(response, "/login/?next=/game_over/1/")

        # Leaderboard view.
        response = self.client.get("/leaderboard/", follow=True)
        self.assertRedirects(response, "/login/?next=/leaderboard/")

    def test_responses_authentication_views(self):
        """Test responses for authentication related views."""
        # Login view.
        response = self.client.get("/login/", follow=True)
        self.assertEquals(response.status_code, 200)

        # Logout view.
        response = self.client.get("/logout/", follow=True)
        self.assertRedirects(response, "/")

        # Registration view.
        response = self.client.get("/register/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirects_user_views(self):
        """Test redirects for user related views."""
        # Users view.
        response = self.client.get("/users/", follow=True)
        self.assertEquals(response.status_code, 404)
        # User detail view.
        response = self.client.get("/users/test/", follow=True)
        self.assertRedirects(response, "/login/?next=/users/test/")
        # Update email view.
        response = self.client.get("/update_email/", follow=True)
        self.assertRedirects(response, "/login/?next=/update_email/")

    def test_redirects_event_views(self):
        """Test redirects for event related views."""
        # Event list view.
        response = self.client.get("/events/", follow=True)
        self.assertRedirects(response, "/login/?next=/events/")
        # Event details view.
        response = self.client.get("/events/1/", follow=True)
        self.assertRedirects(response, "/login/?next=/events/1/")
        # Event creation view.
        response = self.client.get("/events/new/", follow=True)
        self.assertRedirects(response, "/login/?next=/events/new/")
        # Event update view.
        response = self.client.get("/events/1/update/", follow=True)
        self.assertRedirects(response, "/login/?next=/events/1/update/")
        # Event deletion view.
        response = self.client.get("/events/1/delete/", follow=True)
        self.assertRedirects(response, "/login/?next=/events/1/delete/")

    def test_redirects_treasure_chest_views(self):
        """Test redirects for treasure chest related views."""
        # Treasure chest list view.
        response = self.client.get("/treasure_chests/", follow=True)
        self.assertRedirects(response, "/login/?next=/treasure_chests/")
        # Treasure chest details view.
        response = self.client.get("/treasure_chests/1/", follow=True)
        self.assertRedirects(response, "/login/?next=/treasure_chests/1/")
        # Treasure chest creation view.
        response = self.client.get("/treasure_chests/new/", follow=True)
        self.assertRedirects(response, "/login/?next=/treasure_chests/new/")
        # Treasure chest update view.
        response = self.client.get("/treasure_chests/1/update/", follow=True)
        self.assertRedirects(response, "/login/?next=/treasure_chests/1/update/")
        # Treasure chest deletion view.
        response = self.client.get("/treasure_chests/1/delete/", follow=True)
        self.assertRedirects(response, "/login/?next=/treasure_chests/1/delete/")


class TestHTTPResponsesAndRedirectsLoggedInPlayer(TestCase):
    """Class for testing HTTP responses and redirects when logged in as a player user."""

    def setUp(self):
        """Setup user and log them in."""
        # Create user.
        user = User.objects.create_user(username="testuser", password="P@s5w0rd")
        user.save()

        # Create player with new user.
        Player.objects.create(user=user).save()

        # Log user in.
        self.client.login(username="testuser", password="P@s5w0rd")
    
    def test_response_home_view(self):
        """Test response for home view."""
        response = self.client.get("/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirect_game_views(self):
        """Test redirects for game related views."""
        # Game list view.
        response = self.client.get("/game/", follow=True)
        self.assertEquals(response.status_code, 200)

        # Game view.
        response = self.client.get("/game/1/", follow=True)
        self.assertEquals(response.status_code, 404)

        # Game over view.
        response = self.client.get("/game_over/", follow=True)
        self.assertEquals(response.status_code, 404)
        response = self.client.get("/game_over/1/", follow=True)
        self.assertEquals(response.status_code, 404)

        # Leaderboard view.
        response = self.client.get("/leaderboard/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_responses_authentication_views(self):
        """Test responses for authentication related views."""
        # Login view.
        response = self.client.get("/login/", follow=True)
        self.assertEquals(response.status_code, 200)

        # Logout view.
        response = self.client.get("/logout/", follow=True)
        self.assertRedirects(response, "/")

        # Registration view.
        response = self.client.get("/register/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirects_user_views(self):
        """Test redirects for user related views."""
        # Users view.
        response = self.client.get("/users/", follow=True)
        self.assertEquals(response.status_code, 404)
        # User detail view.
        response = self.client.get("/users/testuser/", follow=True)
        self.assertEquals(response.status_code, 200)
        # Update email view.
        response = self.client.get("/update_email/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirects_event_views(self):
        """Test redirects for event related views."""
        # Event list view.
        response = self.client.get("/events/", follow=True)
        self.assertEquals(response.status_code, 200)
        # Event details view.
        response = self.client.get("/events/1/", follow=True)
        self.assertEquals(response.status_code, 404)
        # Event creation view.
        response = self.client.get("/events/new/", follow=True)
        self.assertEquals(response.status_code, 403)
        # Event update view.
        response = self.client.get("/events/1/update/", follow=True)
        self.assertEquals(response.status_code, 403)
        # Event deletion view.
        response = self.client.get("/events/1/delete/", follow=True)
        self.assertEquals(response.status_code, 403)
    
    def test_redirects_treasure_chest_views(self):
        """Test redirects for treasure chest related views."""
        # Treasure chest list view.
        response = self.client.get("/treasure_chests/", follow=True)
        self.assertEquals(response.status_code, 403)
        # Treasure chest details view.
        response = self.client.get("/treasure_chests/1/", follow=True)
        self.assertEquals(response.status_code, 403)
        # Treasure chest creation view.
        response = self.client.get("/treasure_chests/new/", follow=True)
        self.assertEquals(response.status_code, 403)
        # Treasure chest update view.
        response = self.client.get("/treasure_chests/1/update/", follow=True)
        self.assertEquals(response.status_code, 403)
        # Treasure chest deletion view.
        response = self.client.get("/treasure_chests/1/delete/", follow=True)
        self.assertEquals(response.status_code, 403)


class TestHTTPResponsesAndRedirectsLoggedInGameMaster(TestCase):
    """Class for testing HTTP responses and redirects when logged in as a game master user."""

    def setUp(self):
        """Setup user and log them in."""
        # Create user.
        user = User.objects.create_user(username="testuser", password="P@s5w0rd")
        user.save()

        # Create player with new user.
        Player.objects.create(user=user, is_game_master=True).save()

        # Log user in.
        self.client.login(username="testuser", password="P@s5w0rd")
    
    def test_response_home_view(self):
        """Test response for home view."""
        response = self.client.get("/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirect_game_views(self):
        """Test redirects for game related views."""
        # Game list view.
        response = self.client.get("/game/", follow=True)
        self.assertEquals(response.status_code, 200)

        # Game view.
        response = self.client.get("/game/1/", follow=True)
        self.assertEquals(response.status_code, 404)

        # Game over view.
        response = self.client.get("/game_over/", follow=True)
        self.assertEquals(response.status_code, 404)
        response = self.client.get("/game_over/1/", follow=True)
        self.assertEquals(response.status_code, 404)

        # Leaderboard view.
        response = self.client.get("/leaderboard/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_responses_authentication_views(self):
        """Test responses for authentication related views."""
        # Login view.
        response = self.client.get("/login/", follow=True)
        self.assertEquals(response.status_code, 200)

        # Logout view.
        response = self.client.get("/logout/", follow=True)
        self.assertRedirects(response, "/")

        # Registration view.
        response = self.client.get("/register/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirects_user_views(self):
        """Test redirects for user related views."""
        # Users view.
        response = self.client.get("/users/", follow=True)
        self.assertEquals(response.status_code, 404)
        # User detail view.
        response = self.client.get("/users/testuser/", follow=True)
        self.assertEquals(response.status_code, 200)
        # Update email view.
        response = self.client.get("/update_email/", follow=True)
        self.assertEquals(response.status_code, 200)

    def test_redirects_event_views(self):
        """Test redirects for event related views."""
        # Event list view.
        response = self.client.get("/events/", follow=True)
        self.assertEquals(response.status_code, 200)
        # Event details view.
        response = self.client.get("/events/1/", follow=True)
        self.assertEquals(response.status_code, 404)
        # Event creation view.
        response = self.client.get("/events/new/", follow=True)
        self.assertEquals(response.status_code, 200)
        # Event update view.
        response = self.client.get("/events/1/update/", follow=True)
        self.assertEquals(response.status_code, 404)
        # Event deletion view.
        response = self.client.get("/events/1/delete/", follow=True)
        self.assertEquals(response.status_code, 200)
    
    def test_redirects_treasure_chest_views(self):
        """Test redirects for treasure chest related views."""
        # Treasure chest list view.
        response = self.client.get("/treasure_chests/", follow=True)
        self.assertEquals(response.status_code, 200)
        # Treasure chest details view.
        response = self.client.get("/treasure_chests/1/", follow=True)
        self.assertEquals(response.status_code, 404)
        # Treasure chest creation view.
        response = self.client.get("/treasure_chests/new/", follow=True)
        self.assertEquals(response.status_code, 200)
        # Treasure chest update view.
        response = self.client.get("/treasure_chests/1/update/", follow=True)
        self.assertEquals(response.status_code, 404)
        # Treasure chest deletion view.
        response = self.client.get("/treasure_chests/1/delete/", follow=True)
        self.assertEquals(response.status_code, 200)
