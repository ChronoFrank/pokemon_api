import requests
import json
from .models import Evolution, Pokemon
from django.conf import settings


def get_pokemon_evolution_chains_count():
    url = settings.EVOLUTION_CHAIN_URL

    response = requests.get(url)
    if response.status_code == 200:
        json_response = json.loads(response.text)
        _count = json_response.get('count')
        return int(_count)


def get_evolution_chain(id):
    url = settings.EVOLUTION_CHAIN_URL
    url += '{0}'.format(id)
    print("Evolution chain -> {0}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        json_response = json.loads(response.text)
        return json_response.get('chain')


def get_pokemon_data(query):
    url = settings.POKEMON_DETAILS_URL + '{0}/'.format(query)
    print(url)

    response = requests.get(url)
    if response.status_code == 404:
        print("Pokemon information not found for {0}".format(query))
        return None
    if response.status_code == 200:
        json_response = json.loads(response.text)
        return json_response


def extract_pokemons_from_evolution_chain_data(pokemon_data):
    if pokemon_data and isinstance(pokemon_data, dict):
        if 'species' in pokemon_data.keys() and pokemon_data.get('species'):
            base_pokemon = save_pokemon_info_in_database(pokemon_data.get('species').get('name'))
            if base_pokemon:
                if 'evolves_to' in pokemon_data.keys() and pokemon_data.get('evolves_to'):
                    for data in pokemon_data.get('evolves_to'):
                        save_evolution_in_database(base_pokemon, data)
                        new_evolution_data = data
                        extract_pokemons_from_evolution_chain_data(new_evolution_data)

    if pokemon_data and isinstance(pokemon_data, list):
        for list_data in pokemon_data:
            extract_pokemons_from_evolution_chain_data(list_data)


def save_pokemon_info_in_database(pokemon_name=None):
    if pokemon_name:
        try:
            pokemon_obj = Pokemon.objects.get(name=pokemon_name)
        except Pokemon.DoesNotExist:
            # save pokemon in database
            print("retreving info for {0}".format(pokemon_name))
            pokemon_data = get_pokemon_data(pokemon_name)
            if pokemon_data:
                info = {
                    'pokemon_id': pokemon_data.get('id'),
                    'name': pokemon_data.get('name'),
                    'height': pokemon_data.get('height'),
                    'weight': pokemon_data.get('weight'),
                }
                for stats in pokemon_data.get('stats'):
                    if '-' in stats.get('stat').get('name'):
                        stat_name = stats.get('stat').get('name').replace('-', '_')
                    else:
                        stat_name = stats.get('stat').get('name')
                    info[stat_name] = stats.get('base_stat')

                print(info)
                pokemon_obj = Pokemon.objects.create(**info)
            else:
                pokemon_obj = None

        return pokemon_obj


def save_evolution_in_database(base_pokemon, evolution_data):
    # save data in evolution model
    # if 'species' in evolution_data.keys() and evolution_data.get('species'):
    evolution_pokemon = save_pokemon_info_in_database(evolution_data.get('species').get('name'))
    try:
        Evolution.objects.get(pokemon__id=base_pokemon.id, evolution_pokemon__id=evolution_pokemon.id)
    except Evolution.DoesNotExist:
        evolution_obj = Evolution()
        evolution_obj.pokemon = base_pokemon
        if evolution_data:
            if 'species' in evolution_data.keys() and evolution_data.get('species'):
                evolution_pokemon = save_pokemon_info_in_database(evolution_data.get('species').get('name'))
                evolution_obj.evolution_pokemon = evolution_pokemon
        evolution_obj.save()


def evolution_chain_crawler(chain_id=None):
    if chain_id:
        evolution_chain_data = get_evolution_chain(id=chain_id)
        if evolution_chain_data:
            extract_pokemons_from_evolution_chain_data(evolution_chain_data)
        else:
            raise Exception("No evolution data for the id provided")

    else:
        evolution_chain_count = get_pokemon_evolution_chains_count()
        for i in range(1, evolution_chain_count+1):
            evolution_chain_data = get_evolution_chain(id=i)
            extract_pokemons_from_evolution_chain_data(evolution_chain_data)

    print("All Done")
