from .views import PokemonViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pokemon', PokemonViewSet)

api_urlpatterns = router.urls