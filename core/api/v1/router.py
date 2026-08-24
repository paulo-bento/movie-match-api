from rest_framework.routers import DefaultRouter
from core.api.v1.viewsets import GeneroViewSet, FilmeViewSet, AvaliacaoViewSet

router = DefaultRouter()
router.register(r'generos', GeneroViewSet, basename='genero')
router.register(r'filmes', FilmeViewSet, basename='filme')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')

urlpatterns = router.urls
