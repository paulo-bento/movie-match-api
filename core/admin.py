from django.contrib import admin
from .models import CustomUser, Genero, Filme, Avaliacao

admin.site.register(CustomUser)
admin.site.register(Genero)
admin.site.register(Filme)
admin.site.register(Avaliacao)
