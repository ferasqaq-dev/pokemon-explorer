from django.contrib import admin
from django.urls import path
from pokemons.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]
