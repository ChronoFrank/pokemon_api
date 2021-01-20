from .serializers import PokemonSerializer
from rest_framework import viewsets, mixins
from pokemons.models import Pokemon

class PokemonViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        Small ViewSet  to handle no admin users
        retrieve:
            Return a serialized Pokemon instance with the respective evolutions.
    """

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    lookup_field = 'name'