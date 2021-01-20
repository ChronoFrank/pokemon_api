from .serializers import PokemonSerializer
from rest_framework import viewsets, mixins
from pokemons.models import Pokemon

class PokemonViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    lookup_field = 'name'