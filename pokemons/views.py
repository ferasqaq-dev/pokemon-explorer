import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def home_view(request):
    url = "https://pokeapi.co/api/v2/pokemon?limit=20" #Fetching the first 20 Pokemon from the PokeAPI
    response = requests.get(url).json()
    
    pokemon_list = []
    
    for result in response['results']:
        name = result['name']
        pokemon_id = result['url'].split('/')[-2]
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png" #Fetching the image of the Pokemon using its ID from the PokeAPI's sprite repository
        
        pokemon_list.append({
            'id': pokemon_id,
            'name': name.capitalize(),
            'image': image_url
        })

    context = {
        'pokemons': pokemon_list
    }
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
    
    context = {
        'id': pokemon_id,
        'name': name,
        'height': height,
        'weight': weight,
        'image': image,
        'types': types,
        'abilities': abilities,
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