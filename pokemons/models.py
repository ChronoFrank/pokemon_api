from django.db import models

# Create your models here.

class Pokemon(models.Model):
    """
    Pokemon basic model to store information about the pokemons and the basic stats
    """
    pokemon_id = models.IntegerField()
    name = models.CharField(max_length=200)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    hp =  models.IntegerField(default=0)
    attack =  models.IntegerField(default=0)
    defense =  models.IntegerField(default=0)
    special_attack =  models.IntegerField(default=0)
    special_defense =  models.IntegerField(default=0)
    speed =  models.IntegerField(default=0)

    def __str__(self):
        return '{0}'.format(self.name)

    @property
    def evolutions(self):
        """
        this method will be set as a property for the class in which we search for the evolution chain of
        the pokemon
        :return: A QuerySet object containing all the 3 level evolutions for the current pokemon
        """
        evolutions_queryset = Evolution.objects.filter(pokemon=self)
        second_evolution_queryset = Evolution.objects.filter(pokemon__id__in=evolutions_queryset.values_list('evolution_pokemon_id',
                                                                                                             flat=True))
        union_query_set = list(evolutions_queryset.values_list('pokemon_id', flat=True)) + \
                          list(second_evolution_queryset.values_list('pokemon_id', flat=True))
        queryset = Evolution.objects.filter(pokemon__id__in=union_query_set)
        return queryset

    @property
    def evolution_type(self):
        """
        this method will be set as a property for the class in which we search for in the evolution model
        for the records in which the current pokemon is registered as a pre-evolution or a evolution.
        :return: str saying if the pokemon is pre-evolution or evolution.
        """
        return 'pre-evolution' if Evolution.objects.filter(pokemon=self).exists() else 'evolution'

class Evolution(models.Model):
    """
    Many to Many model to handle all available evolutions of one Pokemon, if a Pokemon
    has not record in this table it means that is the final evolution in the chain or the pokemon
    does not have evolution.
    """
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='base_pokemon')
    evolution_pokemon = models.ForeignKey(Pokemon, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(self.pokemon.name, self.evolution_pokemon.name)

