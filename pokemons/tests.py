from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import FavoritePokemon

class PokemonExplorerTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "SecurePass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        login_successful = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_successful)

    def test_prevent_duplicate_favorites(self):
        
        FavoritePokemon.objects.create(user=self.user, pokemon_id=25, pokemon_name="Pikachu")
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            FavoritePokemon.objects.create(user=self.user, pokemon_id=25, pokemon_name="Pikachu")

    def test_toggle_favorite_requires_login(self):
        response = self.client.get(reverse('toggle_favorite', args=[25]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)