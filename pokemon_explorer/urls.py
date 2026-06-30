from django.contrib import admin
from django.urls import path
from pokemons.views import (
    HomeView, PokemonDetailView, ToggleFavoriteView,
    FavoritesListView, RegisterView, LoginView, LogoutView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('pokemon/<int:pokemon_id>/', PokemonDetailView.as_view(), name='pokemon_detail'),
    path('favorite/<int:pokemon_id>/', ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('favorites/', FavoritesListView.as_view(), name='favorites_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]