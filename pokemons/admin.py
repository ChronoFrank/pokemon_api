from django.contrib import admin

# Register your models here.
from .models import Pokemon, Evolution

class PokemonsAdmin(admin.ModelAdmin):
    list_display = ('pokemon_id', 'name', )
    search_fields = ('name', )

class EvolutionsAdmin(admin.ModelAdmin):
    list_display = ('pokemon', )
    raw_id_fields = ('pokemon', 'evolution_pokemon')
    search_fields = ('pokemon__name', )


admin.site.register(Pokemon, PokemonsAdmin)
admin.site.register(Evolution, EvolutionsAdmin)