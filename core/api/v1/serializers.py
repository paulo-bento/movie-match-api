from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Genero, Filme, Avaliacao
from django.db.models import Avg

User = get_user_model()

# Gênero
class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ['id', 'nome', 'descricao', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# Filme
class FilmeSerializer(serializers.ModelSerializer):
    generos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genero.objects.all()
    )
    generos_detalhes = GeneroSerializer(source='generos', many=True, read_only=True)
    media_nota = serializers.SerializerMethodField()
    total_avaliacoes = serializers.SerializerMethodField()

    class Meta:
        model = Filme
        fields = [
            'id', 'titulo', 'descricao', 'ano_lancamento',
            'generos', 'generos_detalhes',
            'capa_url', 'media_nota', 'total_avaliacoes',
            'created_at', 'updated_at', 'is_deleted'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_deleted']

    def get_media_nota(self, obj):
        return obj.avaliacoes.aggregate(media=Avg('nota'))['media']

    def get_total_avaliacoes(self, obj):
        return obj.avaliacoes.count()

# Avaliação
class AvaliacaoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)
    filme_titulo = serializers.CharField(source='filme.titulo', read_only=True)

    class Meta:
        model = Avaliacao
        fields = [
            'id', 'usuario', 'usuario_email',
            'filme', 'filme_titulo',
            'nota', 'comentario',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'usuario']

    def validate(self, data):
        # Impede que o usuário avalie o mesmo filme duas vezes
        usuario = self.context['request'].user
        filme = data.get('filme')
        if self.instance is None:  # criação
            if Avaliacao.objects.filter(usuario=usuario, filme=filme).exists():
                raise serializers.ValidationError("Você já avaliou este filme.")
        return data

# Usuário
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'data_nascimento']
