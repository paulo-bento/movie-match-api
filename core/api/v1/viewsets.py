from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from core.models import Genero, Filme, Avaliacao
from core.api.v1.serializers import (
    GeneroSerializer, FilmeSerializer, AvaliacaoSerializer
)
from core.api.v1.permissions import IsOwnerOrReadOnly

# Gênero
class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nome']
    filterset_fields = ['nome']

    # Cache para listagem
    @method_decorator(cache_page(60 * 5))  # 5 minutos
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Filme
class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['titulo', 'descricao']
    filterset_fields = ['ano_lancamento', 'generos']

    # Cache para listagem
    @method_decorator(cache_page(60 * 5))  # 5 minutos
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Endpoint customizado: filmes recomendados (maior média de nota)
    @action(detail=False, methods=['get'], url_path='recomendados')
    def recomendados(self, request):
        filmes = Filme.objects.annotate(
            media_nota=Avg('avaliacoes__nota'),
            total_avaliacoes=Count('avaliacoes')
        ).filter(total_avaliacoes__gte=1).order_by('-media_nota')[:10]
        serializer = self.get_serializer(filmes, many=True)
        return Response(serializer.data)

# Avaliação
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'filme', 'nota']

    def get_queryset(self):
        # Apenas avaliações ativas (sem soft delete)
        return super().get_queryset()

    # Cache para listagem
    @method_decorator(cache_page(60 * 2))  # 2 minutos
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
