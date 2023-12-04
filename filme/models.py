from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import PIL


# ('armazena_no_banco', 'aparece_pro_user')
LISTA_CATEGORIAS = (
    ("Analises", "Análises"),
    ("Programacao", "Programação"),
    ("Apresentacao", "Apresentação"),
    ("Outros", "Outros"),
)


# Filme
class Filme(models.Model):
    title = models.CharField(max_length=100)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    thumb = models.ImageField(upload_to='thumb_filmes')
    # Text É um bloco para escrever
    descricao = models.TextField(max_length=1000)
    qtd_views = models.IntegerField(default=0)
    date_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title


class Episodio(models.Model):
    # um pra muitos ('Nome da tabela', related_name='', on_delete=models.CASCADE) ---- se for muitos para muitos é models.ManyToManyField
    filme = models.ForeignKey(
        'Filme', related_name='episodios', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self) -> str:
        return self.filme.title + " - " + self.title


class User(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme") #muitos users podem ver vários fil. ou um user pode ver vários fil.
