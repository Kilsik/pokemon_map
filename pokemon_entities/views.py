import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.http import request
from django.utils import timezone

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)
TIME_ZONE = 'Europe/Moscow'


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    today = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=today,
        disappeared_at__gt=today)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    today = timezone.localtime()

    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon,
        appeared_at__lte=today, disappeared_at__gt=today)
    for pokemon_entity in pokemon_entities:

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.image.url)
        )
    previous_evolution = requested_pokemon.previous_evolution
    next_evolution = requested_pokemon.next_evolutions.filter(
            previous_evolution=requested_pokemon.id).first()
    previous_pokemon = None
    next_pokemon = None
    if previous_evolution:
        previous_pokemon = {
            'pokemon_id': previous_evolution.id,
            'img_url': previous_evolution.image.url,
            'title_ru': previous_evolution.title_ru,
            }
    if next_evolution:
        next_pokemon = {
        'pokemon_id': next_evolution.id,
        'img_url': next_evolution.image.url,
        'title_ru': next_evolution.title_ru,
        }
    pokemon_on_page = {
        'img_url': requested_pokemon.image.url,
        'title_ru': requested_pokemon.title_ru,
        'description': requested_pokemon.description,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'previous_evolution': previous_pokemon,
        'next_evolution': next_pokemon
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page,
    })
