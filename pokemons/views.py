import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from pokemons.models import Pokemon, FavoritePokemon

class HomeView(TemplateView):
    template_name = "pokemons/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        query_name = request.GET.get("search", "").strip().lower()

        queryset = Pokemon.objects.all().order_by("pokemon_id")
        if query_name:
            queryset = queryset.filter(name__icontains=query_name)

        limit = 12
        page = int(request.GET.get("page", "1"))
        total_count = queryset.count()
        total_pages = (total_count + limit - 1) // limit

        offset = (page - 1) * limit
        paginated_queryset = queryset[offset : offset + limit]

        user_favs = []
        if request.user.is_authenticated:
            user_favs = list(FavoritePokemon.objects.filter(user=request.user).values_list("pokemon_id", flat=True))

        pokemon_list = []
        for p in paginated_queryset:
            pokemon_list.append({
                "id": p.pokemon_id,
                "name": p.name.capitalize(),
                "image": p.image,
                "is_favorite": p.pokemon_id in user_favs,
            })

        context.update({
            "pokemons": pokemon_list,
            "query_name": request.GET.get("search", ""),
            "current_page": page,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "next_page": page + 1,
            "prev_page": page - 1,
            "total_count": total_count,
        })
        return context

class PokemonDetailView(View):
    def get(self, request, pokemon_id):
        pokemon = get_object_or_404(Pokemon, pokemon_id=pokemon_id)
        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = FavoritePokemon.objects.filter(user=request.user, pokemon_id=pokemon_id).exists()

        context = {
            "id": pokemon.pokemon_id,
            "name": pokemon.name.capitalize(),
            "height": pokemon.height,
            "weight": pokemon.weight,
            "image": pokemon.image,
            "types": pokemon.types if pokemon.types else "Normal",
            "abilities": pokemon.abilities if pokemon.abilities else "None",
            "is_favorite": is_favorite,
        }
        return render(request, "pokemons/detail.html", context)

class ToggleFavoriteView(LoginRequiredMixin, View):
    def get(self, request, pokemon_id):
        pokemon = get_object_or_404(Pokemon, pokemon_id=pokemon_id)
        fav, created = FavoritePokemon.objects.get_or_create(
            user=request.user,
            pokemon_id=pokemon_id,
            defaults={"pokemon_name": pokemon.name, "pokemon_obj": pokemon}
        )
        if not created:
            fav.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))

class FavoritesListView(LoginRequiredMixin, TemplateView):
    template_name = "pokemons/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fav_objects = FavoritePokemon.objects.filter(user=self.request.user)
        pokemons = []
        for fav in fav_objects:
            # نضمن سحب الصورة والبيانات الأساسية حتى لو مخزنة في الـ Favorite
            p_obj = fav.pokemon_obj
            pokemons.append({
                "id": fav.pokemon_id,
                "name": fav.pokemon_name.capitalize(),
                "image": p_obj.image if p_obj else "",
            })
        context["pokemons"] = pokemons
        return context

class RegisterView(FormView):
    template_name = "pokemons/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")

class LoginView(FormView):
    template_name = "pokemons/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect("/")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")