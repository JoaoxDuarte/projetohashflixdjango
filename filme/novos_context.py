from .models import Filme


def list_filmes_recentes(request):
    # ('-data_criacao') e para pegar a data decrescente
    lista_filmes = Filme.objects.all().order_by('-date_criacao')[0:8]
    # Se não usasse o def filme_destaque, seria asssim:
    # filmes_destaque = lista_filmes[0]
    # return {"list_filmes_recentes": lista_filmes, "filme_destaque": filme_destaque}
    return {"list_filmes_recentes": lista_filmes}


def list_filmes_em_alta(request):
    lista_filmes = Filme.objects.all().order_by('-qtd_views')[0:8]
    return {"list_filmes_em_alta": lista_filmes}

# Se não usasse o o list_filmes_recetes, seria asssim:
def filme_destaque(request):
    filme = Filme.objects.order_by('-date_criacao')
    if filme:
        filme = Filme.objects.order_by('-date_criacao')[0]
    else:
        filme = None
    return {"filme_destaque": filme}
