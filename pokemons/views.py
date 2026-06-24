import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache


from pokemons.models import FavoritePokemon

def home_view(request):
    query_name = request.GET.get('search', '').strip().lower()
    
    offset = request.GET.get('offset', '0')
    limit = 20
    cache_key = f'pokeapi_offset_{offset}_limit_{limit}'
    response = cache.get(cache_key)
    
    if not response:
        url = "https://pokeapi.co/api/v2/pokemon?limit=150" if query_name else f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
        try:
            response = requests.get(url).json()
            if not query_name:
                cache.set(cache_key, response, timeout=300)
        except Exception:
            response = {'results': []}

    user_favs = []
    if request.user.is_authenticated:
        user_favs = list(FavoritePokemon.objects.filter(user=request.user).values_list('pokemon_id', flat=True))
    
    pokemon_list = []
    for result in response.get('results', []):
        name = result['name']
        
        if query_name and query_name not in name:
            continue
            
        pokemon_id = int(result['url'].split('/')[-2])
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
        
        pokemon_list.append({
            'id': pokemon_id,
            'name': name.capitalize(),
            'image': image_url,
            'is_favorite': pokemon_id in user_favs
        })

    current_offset = int(offset)
    next_offset = current_offset + limit if response.get('next') else None
    prev_offset = current_offset - limit if current_offset >= limit else None

    context = {
        'pokemons': pokemon_list,
        'query_name': request.GET.get('search', ''),
        'next_offset': next_offset,
        'prev_offset': prev_offset,
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'pokemons/pokemon_list_partial.html', context)
        
    return render(request, 'pokemons/home.html', context)

def pokemon_detail_view(request, pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url).json()
    
    name = response['name'].capitalize()
    height = response['height']
    weight = response['weight']
    image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    types = [t['type']['name'].capitalize() for t in response['types']]
    abilities = [a['ability']['name'].capitalize() for a in response['abilities']]
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoritePokemon.objects.filter(user=request.user, pokemon_id=pokemon_id).exists()
    
    context = {
        'id': pokemon_id, 'name': name, 'height': height, 'weight': weight,
        'image': image, 'types': types, 'abilities': abilities, 'is_favorite': is_favorite
    }
    return render(request, 'pokemons/detail.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'pokemons/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'pokemons/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
    return redirect('home')

@login_required(login_url='login')
def toggle_favorite_view(request, pokemon_id):
    pokemon_name = request.GET.get('name', 'Pokemon')
    
    fav_exists = FavoritePokemon.objects.filter(user=request.user, pokemon_id=pokemon_id).exists()
    
    if fav_exists:
        FavoritePokemon.objects.filter(user=request.user, pokemon_id=pokemon_id).delete()
        action = "removed"
    else:
        FavoritePokemon.objects.create(user=request.user, pokemon_id=pokemon_id, pokemon_name=pokemon_name)
        action = "added"
    
    return JsonResponse({"status": "success", "action": action})

@login_required(login_url='login')
def favorites_list_view(request):
    fav_objects = FavoritePokemon.objects.filter(user=request.user)
    
    pokemons = []
    for fav in fav_objects:
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{fav.pokemon_id}.png"
        pokemons.append({
            'id': fav.pokemon_id,
            'name': fav.pokemon_name,
            'image': image_url,
            'is_favorite': True
        })
        
    return render(request, 'pokemons/favorites.html', {'pokemons': pokemons})

    