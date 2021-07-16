from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput
from .models import Producao, Artesao, Categoria, Fornecedor, Gastos, GastosProd, Instrucoes, MateriaPrima, MpProd, ProdVendido, ProdutoStock, TipoProd


# Classe formulário Produção
class ProducaoForm(ModelForm):
    class Meta:
        model = Producao
        fields = '__all__'

        widgets = {
            'artesao_codigo': forms.HiddenInput(attrs={"initial": 1}),
            'tipo_prod_codigo': forms.HiddenInput(attrs={"initial": 1}),
            'gastos_prod_codigo': forms.Select(attrs={'class': 'form-control'}),
            'mp_prod_codigo': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escreva o nome do produto...'}),
            'tempo_producao': forms.NumberInput(attrs={'class': 'form-control'}),
            'custo_hora_producao': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'gastos_prod_codigo': 'Gasto',
            'mp_prod_codigo': 'Matéria Primas',
            'tempo_producao': 'Tempo de Produção (minutos)',
            'custo_hora_producao': 'Custo Hora',
        }


# Classe formulário Tipo Produto
class TipoProdForm(ModelForm):
    class Meta:
        model = TipoProd
        fields = '__all__'
        exclude = 'custo_producao',

        widgets = {
            'codigo': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do produto...'}),
            'custo_producao': forms.NumberInput(attrs={'class': 'form-control'}),
            'lucro': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '1', 'max': '100'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria_codigo': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'nome': 'Nome',
            'imagem': 'Imagem ',
            'custo_producao': 'Custo de Produção',
            'lucro': 'Lucro (%)',
            'preco': 'Preço',
            'categoria_codigo': 'Categoria',
        }


# Classe formulário Artesão
class ArtesaoForm(UserCreationForm):
    class Meta:
        model = Artesao
        fields = ("username", "first_name", "last_name", "email",)

    username = forms.CharField(label='Username:', min_length=4, max_length=150)
    first_name = forms.CharField(label='Nome:', min_length=1, max_length=150)
    last_name = forms.CharField(label='Apelido:', min_length=1, max_length=150)
    email = forms.EmailField(label='Email:')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar password', widget=forms.PasswordInput)


# Classe formulário Fornecedor
class FornecedorForm(ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'

        widgets = {
            'nipc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o NIPC...'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email...'}),
            'morada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a morada...'}),
            'n_porta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o número da porta...'}),
            'cod_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o código postal...'}),
            'localidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a localidade...'}),
            'concelho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o concelho...'}),
            'telefone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ex.:210000000...'}),
        }

        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'morada': 'Morada',
            'n_porta': 'Nº Porta',
            'cod_postal': 'Código Postal',
            'localidade': 'Localidade',
            'concelho': 'Concelho',
            'telefone': 'Telefone',

        }

        # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'email': 'nome@endereco.com',
            'cod_postal': '1234-56',
        }


# Classe formulário Gastos
class GastosForm(ModelForm):
    class Meta:
        model = Gastos
        fields = '__all__'

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Água'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 20,32'}),
            'codigo': forms.HiddenInput(attrs={'class': 'form-control', 'value': 1}),
            'artesao_codigo': forms.HiddenInput(),
        }

        labels = {
            'nome': 'Nome',
            'valor': 'Valor',
        }


# Classe formulário Gastos de Produção
class GastosProdForm(ModelForm):
    class Meta:
        model = GastosProd
        fields = '__all__'

        widgets = {
            'codigo': forms.HiddenInput(),
            'gastos_codigo': forms.Select(attrs={'class': 'form-control'}),
            'percentagem': forms.NumberInput(attrs={'class': 'form-control'}),
            'producao_artesao_codigo': forms.HiddenInput(),
            'producao_tipo_prod_codigo': forms.HiddenInput(),
        }

        labels = {
            'gastos_codigo': 'Gasto Produção',
            'percentagem': 'Percentagem (%)',
        }

        # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'percentagem': 'Percentagem do valor total do gasto utilizada para esta produção',
        }


# Classe formulário Instruções
class InstrucoesForm(ModelForm):
    class Meta:
        model = Instrucoes
        fields = '__all__'

        widgets = {
            'codigo': forms.HiddenInput(attrs={'class': 'form-control', 'value': 1}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da instrução...'}),
        }

        labels = {
            'instrucao': 'Ficheiro de Instruções',
            'imagem': 'Imagem',
        }


# Classe formulário Matéria-prima
class MateriaPrimaForm(ModelForm):
    class Meta:
        model = MateriaPrima
        fields = '__all__'

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Madeira'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'unid_medida_codigo': forms.Select(attrs={'class': 'form-control'}),
            'especificacoes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Madeira em carvalho'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cor': TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'alerta_qt_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'codigo': forms.HiddenInput(attrs={'class': 'form-control', 'value': 1}),
            'artesao_codigo': forms.HiddenInput(),
        }

        labels = {
            'nome': 'Nome',
            'quantidade': 'Quantidade',
            'unid_medida_codigo': 'Unidade de Medida',
            'especificacoes': 'Especificações',
            'preco': 'Preço Total',
            'cor': 'Cor',
            'alerta_qt_minima': 'Quantidade Mínima para Alerta de Estoque',
        }


# Classe formulário Matéria-prima de Produção
class MpProdForm(ModelForm):
    class Meta:
        model = MpProd
        fields = '__all__'

        widgets = {
            'codigo': forms.HiddenInput(),
            'materia_prima_codigo': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'unid_medida_codigo': forms.Select(attrs={'class': 'form-control'}),
            'producao_artesao_codigo': forms.HiddenInput(),
            'producao_tipo_prod_codigo': forms.HiddenInput(),
        }

        labels = {
            'materia_prima_codigo': 'Matéria Prima',
            'quantidade': 'Quantidade Utilizada',
            'unid_medida_codigo': 'Unidade de Medida da Quantidade Utilizada',
        }


# Classe formulário Produto Vendido
class ProdVendidoForm(ModelForm):
    class Meta:
        model = ProdVendido
        fields = '__all__'

        widgets = {
            'produto_stock_tipo_prod_codigo': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o local de venda...'}),
            'preco_final': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_venda': forms.HiddenInput(attrs={'class': 'form-control', 'value': 1}),
        }

        # ver quantidade e unidade de medida

        labels = {
            'produto_stock_tipo_prod_codigo': 'Produto',
            'data': 'Data de venda',
            'local': 'Local de venda',
            'preco_final': 'Preço final de venda',

        }


# Classe formulário Produto Stock
class ProdutoStockForm(ModelForm):
    class Meta:
        model = ProdutoStock
        fields = '__all__'
        exclude = ['tipo_prod_codigo']

        widgets = {

            'quantidade': forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5'}),
            'preco': forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5'}),
        }

        labels = {

            'quantidade': 'Quantidade',
            'preco': 'Preço',

        }
