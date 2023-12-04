from django.urls import path,reverse_lazy
from .views import Homepage, Homefilmes, Detalhesfilme, Pesquisafilme, Pagperfil, Criarconta
# homepage, homefilmes
# o nome tem q ser diferente pois já há outro views(.views) - AULA (36)
from django.contrib.auth import views as auth_view

app_name = 'filme'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', Homefilmes.as_view(), name='homefilmes'),
    # int:pk pqnã é para todos os filmes
    path('filmes/<int:pk>', Detalhesfilme.as_view(), name='detalhesfilme'),
    path('pesquisa/', Pesquisafilme.as_view(), name='pesquisafilme'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('editperfil/<int:pk>', Pagperfil.as_view(), name='editperfil'),
    path('criarconta/', Criarconta.as_view(), name='criarconta'),
    # template_name='editperfil.html' para reaproveitar, se quise-se outras funcionabilidades, teria que criar outra
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(
        template_name='editperfil.html', success_url=reverse_lazy('filme:homefilmes')), name='mudarsenha'),

]


# path('', homepage) - se fosse utiliza minha de em vez da class,
# path('filmes/', homefilmes),
