from django.db import models

# Create your models here.

class Pokemon(models.Model):
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
        evolutions_queryset = Evolution.objects.filter(pokemon=self)
        second_evolution_queryset = Evolution.objects.filter(pokemon__id__in=evolutions_queryset.values_list('evolution_pokemon_id',
                                                                                                             flat=True))
        union_query_set = list(evolutions_queryset.values_list('pokemon_id', flat=True)) + \
                          list(second_evolution_queryset.values_list('pokemon_id', flat=True))
        queryset = Evolution.objects.filter(pokemon__id__in=union_query_set)
        return queryset

    @property
    def evolution_type(self):
        return 'pre-evolution' if Evolution.objects.filter(pokemon=self).exists() else 'evolution'

class Evolution(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='base_pokemon')
    evolution_pokemon = models.ForeignKey(Pokemon, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(self.pokemon.name, self.evolution_pokemon.name)

