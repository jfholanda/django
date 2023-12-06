from django.db import models
from django.contrib.auth.models import User
from comentarios.models import Comentario
from atracoes.models import Atracao

class Avaliacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField(null=True, blank=True)
    nota = models.DecimalField(decimal_places=2, max_digits=3)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Avaliação: {self.usuario.username} - {self.nota}>"
