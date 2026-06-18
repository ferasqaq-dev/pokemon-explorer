import requests
from django.shortcuts import render

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