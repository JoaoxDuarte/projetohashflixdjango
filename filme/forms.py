from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

# O forms precisa ser importado no VIEWS (CriarContaForm) e o FormView
# Sub classe da classe UserCreationForm

# AULA (40)


class CriarContaForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Necessário para dizer qual modelo deve-se USAR COMO REFERÊNCIA/BASE
    class Meta:
        model = User
        # senha e confirmação de senha
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado em outra conta! Por favor, utilize outro endereço de e-mail.")
        return email

# A função "clean_email()" checa no banco de dados se o e-mail já existe na tabela de usuários.
# Em caso de existir, retorna a mensagem e bloqueia a criação da conta; inversamente, se o e-mail não existe, a conta é criada.


# Form padrão do Django
class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)
