from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# BaseModel (Auditoria) 
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Soft Delete Manager
class SoftDeleteQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(is_deleted=False)

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).ativos()

    def all_objects(self):
        return super().get_queryset()

# Custom User
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

# Gênero 
class Genero(BaseModel):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.nome

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        ordering = ['nome']

# Filme
class Filme(BaseModel):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    ano_lancamento = models.PositiveIntegerField()
    generos = models.ManyToManyField(Genero, related_name='filmes')
    capa_url = models.URLField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.titulo

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        ordering = ['-ano_lancamento', 'titulo']

# Avaliação
class Avaliacao(BaseModel):
    class Nota(models.IntegerChoices):
        UM = 1, '1 - Péssimo'
        DOIS = 2, '2 - Ruim'
        TRES = 3, '3 - Regular'
        QUATRO = 4, '4 - Bom'
        CINCO = 5, '5 - Excelente'

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='avaliacoes')
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.PositiveSmallIntegerField(choices=Nota.choices, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.usuario.email} - {self.filme.titulo} - {self.nota}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        unique_together = ['usuario', 'filme']  # cada usuário avalia um filme uma vez
        ordering = ['-created_at']