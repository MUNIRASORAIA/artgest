from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection

from artgest.forms import ProducaoForm, MateriaPrimaForm, TipoProdForm, GastosForm, FornecedorForm, InstrucoesForm, \
    ProdVendidoForm, GastosProdForm, MpProdForm, ArtesaoForm
from artgest.models import Producao, MateriaPrima, Gastos, Fornecedor, Instrucoes, ProdVendido, TipoProd, GastosProd, \
    Alerta, Artesao


# faz uma verificação de autenticação e redireciona para a página de utilizador (userpage.html) se autenticado
# ou a página inícial (home.html) se não autenticado
def home_page_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:userpage'))

    registar_form = ArtesaoForm(request.POST or None)

    if registar_form.is_valid():
        registar_form.save()
        messages.success(request, 'Utilizador registado com êxito! Já poderá efetuar o Login.', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:home'))
    elif request.method == 'POST' and not registar_form.is_valid():
        print(messages.error())
        messages.error()

    context = {
        'titulo': 'Home',
        'registar_form': registar_form,

    }

    return render(request, 'artgest/home.html', context)


# Recebe dados de autenticação através de um método POST e chama o método de autenticação do Django
# Reireciona para a página de utilizador (userpage.html) se autenticado
# ou para a página inícial (home.html) se não autenticado
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('artgest:userpage'))

    return HttpResponseRedirect(reverse('artgest:home'))


# Chama o método logout() do Django e redireciona para a página inicial (home.html)
def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('artgest:home'))


# Retorna a página sobre (sobre.html).
def sobre_page_view(request):
    context = {
        'titulo': 'Sobre Nós'
    }

    return render(request, 'artgest/sobre.html', context)


# Retorna a página informações (info.html)
def info_page_view(request):
    context = {
        'titulo': 'Informações'
    }

    return render(request, 'artgest/info.html', context)


# faz uma verificação de autenticação e redireciona para a página de utilizador (userpage.html) se autenticado
# ou a página inícial (home.html) se não autenticado
def userpage_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    context = {
        'titulo': 'Userpage',
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/userpage.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, cria um form de tipo de produto e redireciona para a página de registar produtos (produtos_registar.html)
def registar_produtos_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    tprod_form = TipoProdForm(request.POST, request.FILES)
    print(tprod_form)
    print(request.POST.get('imagem'))
    print('request.FILES')
    print(request.FILES)
    if tprod_form.is_valid():

        with connection.cursor() as cursor:
            cursor.execute("SELECT TIPO_PROD_COD_SEQ.NEXTVAL FROM DUAL;")
            nextval = cursor.fetchone()
        tipoprod_codigo = nextval[0]
        cursor.close()
        instancia = tprod_form.save(commit=False)
        instancia.codigo = tipoprod_codigo
        instancia.save()
        return redirect('artgest:produtos_visualizar', tipoprod_codigo)

    elif request.method == 'POST' and not tprod_form.is_valid():
        messages.error(request, 'Não é possível avançar. Este tipo de produto já existe.', extra_tags='Atenção')
        # print(messages.error)

    context = {
        'titulo': 'Registar Tipo de Produto',
        'tprod_form': tprod_form,
        'artesao_codigo': request.user.codigo

    }

    return render(request, 'artgest/produtos_registar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, cria forms de Producao, Matérias-Primas e Gastos, e redireciona para a página de visualizar produtos (produtos_visualizar.html)
def visualizar_produtos_page_view(request, tipoprod_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    user_codigo = request.user.codigo

    try:
        producao = Producao.objects.get(artesao_codigo=user_codigo, tipo_prod_codigo=tipoprod_codigo)
        print('produto seleccionado')
    except:
        producao = None

    try:
        mpprod = MateriaPrima.objects.get(producao_artesao_codigo=user_codigo, producao_tipo_prod_codigo=tipoprod_codigo).values()
        print('materia prima seleccionado')
    except:
        mpprod = None

    try:
        gastosprod = GastosProd.objects.get(producao_artesao_codigo=user_codigo, producao_tipo_prod_codigo=tipoprod_codigo).values()
        print('gasto seleccionado')
    except:
        gastosprod = None

    tipoproduto = TipoProd.objects.get(codigo=tipoprod_codigo)
    tprod_form = TipoProdForm(request.POST or None, instance=tipoproduto)
    producao_form = ProducaoForm(request.POST or None)
    mpprod_form = MpProdForm(request.POST or None)
    gastosprod_form = GastosProdForm(request.POST or None)

    print(tprod_form)
    print(request.POST)
    print(request.FILES)

    context = {
        'titulo': 'Finalizar Registo do Tipo de Produto',
        'tipoproduto': tipoproduto,
        'tprod_form': tprod_form,
        'producao': producao,
        'mpprod': mpprod,
        'gastosprod': gastosprod,
        'producao_form': producao_form,
        'mpprod_form': mpprod_form,
        'gastosprod_form': gastosprod_form,
        'user_codigo': user_codigo,
        'artesao_codigo': request.user.codigo
    }

    if 'inserir-producao-bd' in request.POST and producao_form.is_valid():
        producao_form.save()
        messages.success(request, 'A Produção foi acrescentada ao Tipo de Produto.', extra_tags='Sucesso')
        # return render(request, 'artgest/produtos_visualizar.html', context)

    if 'inserir-mpprod-bd' in request.POST and mpprod_form.is_valid():
        mpprod_form.save()
        messages.success(request, 'A matéria-prima foi acrescentada ao Tipo de Produto.', extra_tags='Sucesso')
        # return render(request, 'artgest/produtos_visualizar.html', context)

    if 'inserir-gasto-bd' in request.POST and gastosprod_form.is_valid():
        gastosprod_form.save()
        messages.success(request, 'O Gasto foi acrescentado ao Tipo de Produto.', extra_tags='Sucesso')
        # return render(request, 'artgest/produtos_visualizar.html', context)

    if tprod_form.is_valid():
        tprod_form.save()
        messages.success(request, 'O Tipo de Produto foi registado com êxito!.', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:produtos_listar'))

    return render(request, 'artgest/produtos_visualizar.html', context)


# def calcula_preco_ideal(email):
#     with connection.cursor() as cursor:
#         cursor.callfunc('utils_pkg.preco_ideal_fnc', [email, 120, 6, 0.5, {'codigo': 1015, 'quantidade': 10, 'unid_medida_codigo': 1012}, 0.1])
#         preco_ideal = cursor.fetchone()
#         cursor.close()
#
#     return preco_ideal


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados para obter e retornar todos os registos
def listar_produtos_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    tiposproduto = TipoProd.objects.all().order_by('-codigo')

    colunas = ['Código', 'Nome', 'Custo de Produção', 'Lucro', 'Preço Unidade', 'Categoria']

    context = {
        'titulo': 'Tipos de Produto',
        'tiposproduto': tiposproduto,
        'colunas': colunas,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/produtos_listar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados, cria um form com base no registo recebido e retorna uma página de edição
# valida o form e insere os dados na base de dados
def editar_produtos_page_view(request, tipoprod_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    tipoproduto = TipoProd.objects.get(pk=tipoprod_codigo)
    tp_form = TipoProdForm(request.POST or None, instance=tipoproduto)
    print(tp_form.is_valid())
    print(request.POST)
    if tp_form.is_valid():
        tp_form.save()
        messages.success(request, 'Tipo de produto editado com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:produtos_listar'))

    context = {
        'titulo': 'Editar Tipo de Produto',
        'tp_form': tp_form,
        'tipoprod_codigo': tipoprod_codigo,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/produtos_editar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz um delete() ao objeto a eliminar
# faz tratamento de exceções
def eliminar_produtos_page_view(request, tipoprod_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    try:
        TipoProd.objects.get(codigo=tipoprod_codigo).delete()
    except:
        messages.error(request, 'Não é possível eliminar este tipo de produto. Existem dependências.',
                       extra_tags='Atenção')
    else:
        messages.success(request, 'O Tipo de Produto foi eliminada com êxito!', extra_tags='Sucesso')
    return HttpResponseRedirect(reverse('artgest:produtos_listar'))


def eliminar_producao_view(request, tipoprod_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))
    user_codigo = request.user.codigo
    try:
        producao = Producao.objects.get(producao_artesao_codigo=user_codigo, producao_tipo_prod_codigo=tipoprod_codigo)
    except:
        messages.error(request, 'Não é possível eliminar este tipo de produto. Existem dependências.',
                       extra_tags='Atenção')
    else:
        messages.success(request, 'O Tipo de Produto foi eliminada com êxito!', extra_tags='Sucesso')
    return HttpResponseRedirect(reverse('artgest:produtos_visualizar'))


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, cria um form de matérias-primas e redireciona para a página de registar matérias-primas (materiasprimas_registar.html)
def registar_materiasprimas_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    mp_form = MateriaPrimaForm(request.POST or None)

    if mp_form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute("SELECT MATERIA_PRIMA_COD_SEQ.NEXTVAL FROM DUAL;")
            nextval = cursor.fetchone()
        codigo_materia_prima = nextval[0]
        cursor.close()
        instancia = mp_form.save(commit=False)
        instancia.codigo = codigo_materia_prima
        instancia.save()

        email = request.user.email
        gera_alertas(email, codigo_materia_prima)
        messages.success(request, 'Matéria-prima registada com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:materiasprimas_registar'))
    elif request.method == 'POST' and not mp_form.is_valid():
        messages.error(request, 'Não é possível registar. Esta matéria-prima já existe.', extra_tags='Atenção')

    context = {
        'titulo': 'Registar Matéria-Prima',
        'mp_form': mp_form,
        'user_codigo': request.user.codigo,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/materiasprimas_registar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados para obter e retornar todos os registos
def listar_materiasprimas_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    materias_primas = MateriaPrima.objects.all().order_by('-codigo')

    colunas = ['Código', 'Nome', 'Quantidade', 'Unidade de Medida', 'Especificações', 'Preço Total', 'Cor',
               'Alerta de Estoque']

    context = {
        'titulo': 'Materias-Primas',
        'materias_primas': materias_primas,
        'colunas': colunas
    }

    return render(request, 'artgest/materiasprimas_listar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados, cria um form com base no registo recebido e retorna uma página de edição
# valida o form e insere os dados na base de dados
def editar_materiasprimas_page_view(request, materia_prima_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    materia_prima = MateriaPrima.objects.get(pk=materia_prima_codigo)
    mp_form = MateriaPrimaForm(request.POST or None, instance=materia_prima)
    if mp_form.is_valid():
        mp_form.save()
        email = request.user.email
        gera_alertas(email, materia_prima_codigo)
        messages.success(request, 'Matéria-prima editada com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:materiasprimas_listar'))

    context = {
        'titulo': 'Editar Materia-Prima',
        'mp_form': mp_form,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/materiasprimas_editar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz um delete() ao objeto a eliminar
# faz tratamento de exceções
def eliminar_materiasprimas_view(request, materia_prima_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    try:
        MateriaPrima.objects.get(codigo=materia_prima_codigo).delete()
    except:
        messages.error(request, 'Não é possível eliminar a matéria-prima. Existem dependências.', extra_tags='Atenção')
    else:
        messages.success(request, 'A matéria-prima foi eliminada com êxito!', extra_tags='Sucesso')
    return HttpResponseRedirect(reverse('artgest:materiasprimas_listar'))


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, cria um form de gastos e redireciona para a página de registar gastos (gastos_registar.html)
def registar_gastos_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    gastos_form = GastosForm(request.POST or None)

    print(gastos_form.is_valid())

    if gastos_form.is_valid():
        gastos_form.save()
        messages.success(request, 'Gasto registado com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:gastos_listar'))
    elif request.method == 'POST' and not gastos_form.is_valid():
        messages.error(request, 'Não é possível registar. Este gasto já existe.', extra_tags='Atenção')

    context = {
        'titulo': 'Registar Gastos',
        'gastos_form': gastos_form,
        'user_codigo': request.user.codigo,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/gastos_registar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados para obter e retornar todos os registos
def listar_gastos_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    gastos = Gastos.objects.all().order_by('-codigo')

    colunas = ['Código', 'Nome', 'Valor']

    context = {
        'titulo': 'Gastos',
        'gastos': gastos,
        'colunas': colunas,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/gastos_listar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados, cria um form com base no registo recebido e retorna uma página de edição
# valida o form e insere os dados na base de dados
def editar_gastos_page_view(request, gasto_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    gasto = Gastos.objects.get(pk=gasto_codigo)
    gastos_form = GastosForm(request.POST or None, instance=gasto)
    if gastos_form.is_valid():
        gastos_form.save()
        messages.success(request, 'Gasto editado com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:gastos_listar'))

    context = {
        'titulo': 'Editar Gastos',
        'gastos_form': gastos_form,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/gastos_editar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz um delete() ao objeto a eliminar
# faz tratamento de exceções
def eliminar_gastos_view(request, gasto_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    try:
        Gastos.objects.get(codigo=gasto_codigo).delete()
    except:
        messages.error(request, 'Não é possível eliminar este gasto. Existe(m) produto(s) associado(s).',
                       extra_tags='Atenção')
    else:
        messages.success(request, 'Gasto eliminado com êxito!', extra_tags='Sucesso')

    return HttpResponseRedirect(reverse('artgest:gastos_listar'))


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, cria um form de fornecedores e redireciona para a página de registar fornecedores (fornecedores_registar.html)
def registar_fornecedores_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    fornecedores_form = FornecedorForm(request.POST or None)

    if fornecedores_form.is_valid():
        fornecedores_form.save()
        messages.success(request, 'Fornecedor registado com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:fornecedores_listar'))
    elif request.method == 'POST' and not fornecedores_form.is_valid():
        messages.error(request, 'Não é possível registar. Este fornecedor já existe.', extra_tags='Atenção')

    context = {
        'titulo': 'Registar Fornecedores',
        'fornecedores_form': fornecedores_form,
        'user_codigo': request.user.codigo,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/fornecedores_registar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados para obter e retornar todos os registos
def listar_fornecedores_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    fornecedores = Fornecedor.objects.all().order_by('nome')

    colunas = ['NIPC', 'Nome', 'Email', 'Morada', 'Nº Porta', 'Código Postal', 'Localidade', 'Concelho', 'Telefone']

    context = {
        'titulo': 'Fornecedores',
        'fornecedores': fornecedores,
        'colunas': colunas,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/fornecedores_listar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados, cria um form com base no registo recebido e retorna uma página de edição
# valida o form e insere os dados na base de dados
def editar_fornecedores_page_view(request, fornecedor_nipc):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    fornecedor = Fornecedor.objects.get(pk=fornecedor_nipc)
    fornecedores_form = FornecedorForm(request.POST or None, instance=fornecedor)

    if fornecedores_form.is_valid():
        fornecedores_form.save()
        messages.success(request, 'Fornecedor editado com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:fornecedores_listar'))

    context = {
        'titulo': 'Editar Fornecedores',
        'fornecedores_form': fornecedores_form,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/fornecedores_editar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz um delete() ao objeto a eliminar
# faz tratamento de exceções
def eliminar_fornecedores_view(request, fornecedor_nipc):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    try:
        Fornecedor.objects.get(nipc=fornecedor_nipc).delete()
    except:
        messages.error(request, 'Não é possível eliminar o fornecedor. Existem dependências.', extra_tags='Atenção')
    else:
        messages.success(request, 'Fornecedor eliminado com êxito!', extra_tags='Sucesso')

    return render(request, 'artgest/fornecedores_listar.html')


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, cria um form de gastos e redireciona para a página de registar gastos (gastos_registar.html)
def registar_instrucoes_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    instrucoes_form = InstrucoesForm(request.POST, request.FILES)
    print(request.POST.get('imagem'))
    print(request.FILES)
    if instrucoes_form.is_valid():
        instrucoes_form.save()
        messages.success(request, 'Instrução registada com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:instrucoes_registar'))
    elif request.method == 'POST' and not instrucoes_form.is_valid():
        messages.error(request, 'Não foi possível registar. Reveja os ficheiros que submeteu.', extra_tags='Atenção')

    context = {
        'titulo': 'Registar Instrução',
        'instrucoes_form': instrucoes_form,
        'user_codigo': request.user.codigo,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/instrucoes_registar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados para obter e retornar todos os registos
def listar_instrucoes_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    instrucoes = Instrucoes.objects.all().order_by('-codigo')

    colunas = ['Nome', 'Instrução', 'Imagem']

    context = {
        'titulo': 'Instruções',
        'instrucoes': instrucoes,
        'colunas': colunas,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/instrucoes_listar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados, cria um form com base no registo recebido e retorna uma página de edição
# valida o form e insere os dados na base de dados
def editar_instrucoes_page_view(request, instrucao_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    materia_prima = Instrucoes.objects.get(pk=instrucao_codigo)
    instrucoes_form = InstrucoesForm(request.POST or None, instance=materia_prima)
    if instrucoes_form.is_valid():
        instrucoes_form.save()
        messages.success(request, 'Instrução editada com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:instrucoes_listar'))

    context = {
        'titulo': 'Editar Instrução',
        'instrucoes_form': instrucoes_form,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/instrucoes_editar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz um delete() ao objeto a eliminar
# faz tratamento de exceções
def eliminar_instrucoes_view(request, instrucao_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    try:
        Instrucoes.objects.get(codigo=instrucao_codigo).delete()
    except:
        messages.error(request, 'Não é possível eliminar esta instrução. Existem dependências.', extra_tags='Atenção')
    else:
        messages.success(request, 'A instrução foi eliminada com êxito!', extra_tags='Sucesso')
    return HttpResponseRedirect(reverse('artgest:instrucoes_listar'))


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, cria um form de produtos vendidos e redireciona para a página de registar produtos vendidos (prodvendidos_registar.html)
def registar_prodvendidos_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    pv_form = ProdVendidoForm(request.POST or None)

    if pv_form.is_valid():
        pv_form.save()
        messages.success(request, 'Produto vendido registada com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:prodvendidos_registar'))

    context = {
        'titulo': 'Registar Produto Vendido',
        'pv_form': pv_form,
        'user_codigo': request.user.codigo,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/prodvendidos_registar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados para obter e retornar todos os registos
def listar_prodvendidos_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    prodvendidos = ProdVendido.objects.all().order_by('-codigo_venda')

    colunas = ['Código', 'Data', 'Local', 'Preço Final', 'Produto Vendido']

    context = {
        'titulo': 'Produtos Vendidos',
        'prodvendidos': prodvendidos,
        'colunas': colunas,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/prodvendidos_listar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz consulta à base de dados, cria um form com base no registo recebido e retorna uma página de edição
# valida o form e insere os dados na base de dados
def editar_prodvendidos_page_view(request, pv_codigo_venda):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    prodvendidos = ProdVendido.objects.get(pk=pv_codigo_venda)
    pv_form = ProdVendidoForm(request.POST or None, instance=prodvendidos)
    if pv_form.is_valid():
        pv_form.save()
        messages.success(request, 'Venda do produto editada com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:prodvendidos_listar'))

    context = {
        'titulo': 'Editar Venda do Produto',
        'pv_form': pv_form,
        'pv_codigo_venda': pv_codigo_venda,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/prodvendidos_editar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz um delete() ao objeto a eliminar
# faz tratamento de exceções
def eliminar_prodvendidos_view(request, pv_codigo_venda):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    try:
        ProdVendido.objects.get(codigo_venda=pv_codigo_venda).delete()
    except:
        messages.error(request, 'Não é possível eliminar esta venda de produto. Existem dependências.',
                       extra_tags='Atenção')
    else:
        messages.success(request, 'A venda do produto foi eliminada com êxito!', extra_tags='Sucesso')
    return HttpResponseRedirect(reverse('artgest:materiasprimas_listar'))


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, retorna a página de relatórios (relatorios.html)
def relatorios_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    email = request.user.email
    vendas_quantidades = relatorio_quantidades_mes(email)
    vendas_mes = relatorio_vendas_mes(email)
    mp_mais_usadas = relatorio_mp_mais_usadas(email)

    context = {
        'titulo': 'Relatórios',
        'vendas_quantidades': vendas_quantidades,
        'vendas_mes': vendas_mes,
        'mp_mais_usadas': mp_mais_usadas,
        'artesao_codigo': request.user.codigo

    }

    return render(request, 'artgest/relatorios.html', context)


# Acede a uma função base de dados e retorna a quantidade de produtos vendidos nos últimos 30 dias, agrupadas por tipo de produto
def relatorio_quantidades_mes(email):

    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM TABLE(UTILS_PKG.RELATORIO_VENDAS_FNC(%s))', [email])
            vendas = dictfetchall(cursor)
        except:
            print('Sem resultados')
        cursor.close()

    return vendas

# Acede a uma função da base de dados e retorna os produtos vendidos nos últimos 30 dias
def relatorio_vendas_mes(email):

    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM TABLE(UTILS_PKG.RELATORIO_PRECOS_VENDA_FNC(%s))', [email])
            vendas = dictfetchall(cursor)
        except:
            print('Sem resultados')
        cursor.close()

    return vendas


# Acede a uma função da base de dados e retorna as 5 matérias-primas mais usadas na produção
def relatorio_mp_mais_usadas(email):

    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM TABLE(UTILS_PKG.RELATORIO_MP_MAIS_USADAS_FNC(%s))', [email])
            materias_primas = dictfetchall(cursor)
            print(materias_primas)
        except:
            print('Sem resultados')
        cursor.close()

    return materias_primas


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, retorna a página dos alertas (alertas.html)
def alertas_page_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    alertas = Alerta.objects.all().order_by('-codigo')

    context = {
        'titulo': 'Alertas',
        'alertas': alertas,
        'artesao_codigo': request.user.codigo
    }

    return render(request, 'artgest/alertas.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, faz um delete() ao objeto a eliminar
def limpa_alerta_page_view(request, alerta_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    Alerta.objects.get(codigo=alerta_codigo).delete()

    return HttpResponseRedirect(reverse('artgest:alertas'))


# def desmarca_alerta(email):
#     with connection.cursor() as cursor:
#         # cursor.callfunc('utils_pkg.preco_ideal_fnc', [email, 120, 6, 0.5, {'codigo': 1015, 'quantidade': 10, 'unid_medida_codigo': 1012}, 0.1])
#         cursor.callproc('utils_pkg.desmarca_alerta_prc', [email, 1015])
#         # preco_ideal = cursor.fetchone()
#         cursor.close()
#
#     # return preco_ideal


# acede a um procedimento da base de dados para gerar os alertas de quantidade mínima em estoque de matérias-primas
def gera_alertas(email, codigo_materia_prima):
    with connection.cursor() as cursor:
        cursor.callproc('utils_pkg.gera_alertas_prc', [email, codigo_materia_prima])
        cursor.close()


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, retorna a página de visualizaçao de perfil do utilizador (perfil_visualizar.html)
def perfil_visualizar_page_view(request, artesao_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    artesao = Artesao.objects.get(pk=artesao_codigo)

    context = {
        'titulo': 'Perfil do Utilizador',
        'artesao': artesao,
        'artesao_codigo': artesao_codigo
    }

    return render(request, 'artgest/perfil_visualizar.html', context)


# faz uma verificação de autenticação e redireciona para a página inícial (home.html) se não autenticado
# se autenticado, retorna a página de editar perfil do utilizador (perfil.html)
def perfil_page_view(request, artesao_codigo):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('artgest:home'))

    artesao = Artesao.objects.get(pk=artesao_codigo)
    artesao_form = ArtesaoForm(request.POST or None, instance=artesao)
    if artesao_form.is_valid():
        artesao_form.save()
        messages.success(request, 'Perfil editado com êxito!', extra_tags='Sucesso')
        return HttpResponseRedirect(reverse('artgest:materiasprimas_listar'))

    context = {
        'titulo': 'Editar Perfil do Utilizador',
        'artesao_form': artesao_form,
        'artesao_codigo': artesao_codigo
    }

    return render(request, 'artgest/perfil.html', context)


# converte um resultado (query set) num dicionário para poder ser consumido num template
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
