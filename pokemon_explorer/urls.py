from django.contrib import admin
from django.urls import path
from pokemons.views import home_view, pokemon_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('pokemon/<int:pokemon_id>/', pokemon_detail_view, name='pokemon_detail'),
]
