from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada: apenas o dono pode editar/deletar.
    """
    def has_object_permission(self, request, view, obj):
        # Métodos seguros (GET, HEAD, OPTIONS) permitidos para qualquer um
        if request.method in permissions.SAFE_METHODS:
            return True
        # O dono é o usuário associado à avaliação
        return obj.usuario == request.user
