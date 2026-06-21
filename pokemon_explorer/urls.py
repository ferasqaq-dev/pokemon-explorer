from django.contrib import admin
from django.urls import path
from pokemons.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('pokemon/<int:pokemon_id>/', pokemon_detail_view, name='pokemon_detail'),
    path('favorite/<int:pokemon_id>/', toggle_favorite_view, name='toggle_favorite'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
