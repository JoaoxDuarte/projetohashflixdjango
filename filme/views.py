from typing import Any
from django import http
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from .models import Filme, User
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# ulr - view - html

#   Function base views -VS- Class base views   #

# def homepage(request):
# return render(request, 'homepage.html')

# A mesma coisa do de cima, só que ele já tem a função de get e de post


class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomepage

    # AULA (37)
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:  # usuario está autenticado
            return redirect('filme:homefilmes')  # redireciona para a home
        else:
            # tem super pq estamos editando, neste caso, função que já existe
            return super().get(request, *args, **kwargs)

# Verificar e redirecionar o user para criar conta
    def get_success_url(self):
        email = self.request.POST.get("email")
        user = User.objects.filter(email=email)
        if user:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


# def homefilmes(request):
    # x- aula 20 -11:20 ou 07:00
    # x-  context = {}
    # x- context['lista_filmes'] = lista_filmes

    # lista_filmes = Filme.objects.all()

    # return render(request, 'homefilmes.html', {'lista_filmes': lista_filmes}) #context

# listview pois é uma lista e LoginRequiredMixin é só pra conseguir acessar a pag se tiver feito login
class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme  # ele já faz tudo q faz em cima automaticamente // model vira um object_list


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhes.html'
    model = Filme  # object -> 1 item do nosso modelo

    # aula (28)
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # descobrir qual o filme ele tá acessando
        filme = self.get_object()
        filme.qtd_views += 1
        # soma 1 nas visualizacoes e salvar
        filme.save()
        user = request.user
        # Não é .append pis é para adicionar no banco de dados e não uma lista no python, ADD, ASSIM COMO O FILTER E ETC, SÃO MÉTODOS PAR BANCO DE DADOS
        user.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)  # Redireciona o user para url final

    # Filmes relacionados #Aula (26)
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        # Preciso pegar o object, então é usado get_object()
        filmes_relacionados = Filme.objects.filter(
            categoria=self.get_object().categoria)[0:5]  # Só pega/limita 5 filmes relacionados
        context["filmes_relacionados"] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    # Edita o object_list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            # self.model aula (32), pois se a model mudar de nome (ex: Filme para Episodio), ele não dá erro
            object_list = self.model.object.filter(
                title__icontains=termo_pesquisa)
            return object_list
        else:
            return None


# LoginreequiredMixin é para só acessar a pagina se estiver logado
class Pagperfil(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "editperfil.html"
    model = User
    fields = ['first_name', 'last_name', 'email']

    def test_func(self):  # user_nao_pode_mudar_perfil_de_outro — importar o UserPassesTestMixin
        user = self.get_object()
        return self.request.user == user

    def get_success_url(self) -> str:
        return reverse('filme:homefilmes')


class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

# O FORM É VALIDO?
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# A funcao quer um link, por isso o reverse e não o redirect


    def get_success_url(self) -> str:
        return reverse('filme:login')
