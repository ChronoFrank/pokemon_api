from django.contrib import admin

# Register your models here.
from .models import Pokemon, BaseStat

class BaseStatsAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_stat',)
    raw_id_fields = ('pokemon',)

class PokemonsAdmin(admin.ModelAdmin):
    list_display = ('pokemon_id', 'name', )
    raw_id_fields = ('evolution', )


admin.site.register(Pokemon, PokemonsAdmin)
admin.site.register(BaseStat, BaseStatsAdmin)