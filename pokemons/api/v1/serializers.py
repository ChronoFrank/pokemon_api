from rest_framework import serializers
from pokemons.models import Pokemon, Evolution


class EvolutionSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField('get_evolution', read_only=True)
    class Meta:
        model = Evolution
        fields = ('info',)

    def get_evolution(self, obj):
        aux = {
            'pokemon_id': obj.evolution_pokemon.pokemon_id,
            'name': obj.evolution_pokemon.name,
            'evolution_type': obj.evolution_pokemon.evolution_type
        }
        return aux

class PokemonSerializer(serializers.ModelSerializer):
    evolutions = EvolutionSerializer(many=True, read_only=True,)
    class Meta:
        model = Pokemon
        fields = ('pokemon_id',
                  'name',
                  'height',
                  'weight',
                  'hp',
                  'attack',
                  'defense',
                  'special_attack',
                  'special_defense',
                  'speed',
                  'evolutions',)
