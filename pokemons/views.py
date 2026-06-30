import requests
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, FormView, TemplateView

from pokemons.models import FavoritePokemon


class HomeView(TemplateView):
    template_name = "pokemons/home.html"

    def get_template_names(self):
        # لدعم الـ Ajax Request والـ partial template كما كان في كودك القديم
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return ["pokemons/pokemon_list_partial.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        query_name = request.GET.get("search", "").strip().lower()
        offset = request.GET.get("offset", "0")
        limit = 20
        cache_key = f"pokeapi_offset_{offset}_limit_{limit}"
        response = cache.get(cache_key)

        if not response:
            url = (
                "https://pokeapi.co/api/v2/pokemon?limit=150"
                if query_name
                else f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
            )
            try:
                response = requests.get(url).json()
                if not query_name:
                    cache.set(cache_key, response, timeout=300)
            except Exception:
                response = {"results": []}

        user_favs = []
        if request.user.is_authenticated:
            user_favs = list(
                FavoritePokemon.objects.filter(user=request.user).values_list(
                    "pokemon_id", flat=True
                )
            )

        pokemon_list = []
        for result in response.get("results", []):
            name = result["name"]

            if query_name and query_name not in name:
                continue

            pokemon_id = int(result["url"].split("/")[-2])
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"

            pokemon_list.append(
                {
                    "id": pokemon_id,
                    "name": name.capitalize(),
                    "image": image_url,
                    "is_favorite": pokemon_id in user_favs,
                }
            )

        current_offset = int(offset)
        next_offset = current_offset + limit if response.get("next") else None
        prev_offset = current_offset - limit if current_offset >= limit else None

        context.update(
            {
                "pokemons": pokemon_list,
                "query_name": request.GET.get("search", ""),
                "next_offset": next_offset,
                "prev_offset": prev_offset,
            }
        )
        return context


class PokemonDetailView(View):
    def get(self, request, pokemon_id):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
        response = requests.get(url).json()

        name = response["name"].capitalize()
        height = response["height"]
        weight = response["weight"]
        image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
        types = [t["type"]["name"].capitalize() for t in response["types"]]
        abilities = [
            a["ability"]["name"].capitalize() for a in response["abilities"]
        ]

        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = FavoritePokemon.objects.filter(
                user=request.user, pokemon_id=pokemon_id
            ).exists()

        context = {
            "id": pokemon_id,
            "name": name,
            "height": height,
            "weight": weight,
            "image": image,
            "types": types,
            "abilities": abilities,
            "is_favorite": is_favorite,
        }
        return render(request, "pokemons/detail.html", context)


class RegisterView(FormView):
    template_name = "pokemons/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginView(FormView):
    template_name = "pokemons/login.html"
    form_class = AuthenticationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect("home")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")

    def post(self, request):
        logout(request)
        return redirect("home")


class ToggleFavoriteView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, pokemon_id):
        pokemon_name = request.GET.get("name", "Pokemon")

        fav_exists = FavoritePokemon.objects.filter(
            user=request.user, pokemon_id=pokemon_id
        ).exists()

        if fav_exists:
            FavoritePokemon.objects.filter(
                user=request.user, pokemon_id=pokemon_id
            ).delete()
            action = "removed"
        else:
            FavoritePokemon.objects.create(
                user=request.user,
                pokemon_id=pokemon_id,
                pokemon_name=pokemon_name,
            )
            action = "added"

        return JsonResponse({"status": "success", "action": action})


class FavoritesListView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "pokemons/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fav_objects = FavoritePokemon.objects.filter(user=self.request.user)

        pokemons = []
        for fav in fav_objects:
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{fav.pokemon_id}.png"
            pokemons.append(
                {
                    "id": fav.pokemon_id,
                    "name": fav.pokemon_name,
                    "image": image_url,
                    "is_favorite": True,
                }
            )

        context["pokemons"] = pokemons
        return context