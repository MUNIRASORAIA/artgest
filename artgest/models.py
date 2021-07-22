# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Classe tabela Alerta
class Alerta(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=30)
    mensagem = models.CharField(max_length=200)
    visto = models.CharField(max_length=1)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    materia_prima_codigo = models.ForeignKey('MateriaPrima', models.DO_NOTHING, db_column='materia_prima_codigo')

    class Meta:
        managed = True
        db_table = 'alerta'

    def __str__(self):
        return f'{self.nome}: {self.mensagem}'


# Classe tabela Artesão
class Artesao(AbstractUser):
    codigo = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254, verbose_name='email address')
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField(default=1)
    date_joined = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'artesao'
        unique_together = (('email', 'username'),)

    def __str__(self):
        return f'{self.username} ({self.email})'


# Classe tabela Categoria
class Categoria(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'categoria'

    def __str__(self):
        return f'{self.nome}'


# Classe tabela Fornecedor
class Fornecedor(models.Model):
    nipc = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    morada = models.CharField(max_length=150)
    n_porta = models.CharField(max_length=10)
    cod_postal = models.CharField(max_length=8)
    localidade = models.CharField(max_length=20)
    concelho = models.CharField(max_length=20)
    telefone = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'fornecedor'

    def __str__(self):
        return f'{self.nome} | NIPC: {self.nipc}'


# Classe tabela Fornecimento
class Fornecimento(models.Model):
    fornecedor_nipc = models.ForeignKey(Fornecedor, models.DO_NOTHING, db_column='fornecedor_nipc')
    materia_prima_codigo = models.OneToOneField('MateriaPrima', models.DO_NOTHING, db_column='materia_prima_codigo', primary_key=True)

    class Meta:
        managed = True
        db_table = 'fornecimento'
        unique_together = (('materia_prima_codigo', 'fornecedor_nipc'),)

    def __str__(self):
        return f'{self.materia_prima_codigo} | Fornecedor: {self.fornecedor_nipc}'


# Classe tabela Gastos
class Gastos(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    artesao_codigo = models.ForeignKey(Artesao, models.DO_NOTHING, db_column='artesao_codigo')

    class Meta:
        managed = True
        db_table = 'gastos'
        unique_together = (('nome', 'artesao_codigo'),)

    def __str__(self):
        return f'{self.nome} | Valor Total: {self.valor}'


# Classe tabela Gastos de Produção
class GastosProd(models.Model):
    codigo = models.IntegerField(primary_key=True)
    # gastos_codigo = models.ForeignKey('Gastos', models.DO_NOTHING)
    gastos_codigo = models.ForeignKey('Gastos', on_delete=models.CASCADE, null=True)
    percentagem = models.FloatField()
    id = models.ForeignKey('Producao', on_delete=models.CASCADE, null=True, db_column='id')
    # producao_artesao_codigo = models.ForeignKey('Producao', models.DO_NOTHING, db_column='producao_artesao_codigo', related_name='gastosprod_artesao_codigo')
    # producao_tipo_prod_codigo = models.ForeignKey('Producao', models.DO_NOTHING, db_column='producao_tipo_prod_codigo', related_name='gastosprod_tipo_prod_codigo')

    class Meta:
        managed = True
        db_table = 'gastos_prod'

    def __str__(self):
        return f'{self.gastos_codigo} | {self.percentagem} %'


# Classe tabela Instruções de uma produção
class InstProd(models.Model):
    tipo_prod_codigo = models.OneToOneField('TipoProd', models.DO_NOTHING, db_column='tipo_prod_codigo', primary_key=True)
    instrucoes_codigo = models.ForeignKey('Instrucoes', models.DO_NOTHING, db_column='instrucoes_codigo')

    class Meta:
        managed = True
        db_table = 'inst_prod'
        unique_together = (('tipo_prod_codigo', 'instrucoes_codigo'),)

    def __str__(self):
        return f'{self.tipo_prod_codigo} | Instrução: {self.instrucoes_codigo}'


# Classe tabela Instruções
class Instrucoes(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(unique=True, max_length=20)
    instrucao = models.FileField(upload_to='documents/instrucoes/')
    imagem = models.ImageField(upload_to='images/instrucoes/')

    class Meta:
        managed = True
        db_table = 'instrucoes'

    def __str__(self):
        return f'{self.nome}'


# Classe tabela Matéria-prima
class MateriaPrima(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(unique=True, max_length=20)
    quantidade = models.FloatField()
    especificacoes = models.CharField(max_length=100, blank=True, null=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    cor = models.CharField(max_length=20)
    alerta_qt_minima = models.FloatField(blank=True, null=True)
    unid_medida_codigo = models.ForeignKey('UnidMedida', models.DO_NOTHING, db_column='unid_medida_codigo')
    artesao_codigo = models.ForeignKey(Artesao, models.DO_NOTHING, db_column='artesao_codigo')

    class Meta:
        managed = True
        db_table = 'materia_prima'
        unique_together = (('nome', 'artesao_codigo'),)

    def __str__(self):
        return f'{self.nome}'


# Classe tabela Matéria-prima de produção
class MpProd(models.Model):
    codigo = models.IntegerField(primary_key=True)
    materia_prima_codigo = models.ForeignKey(MateriaPrima, models.DO_NOTHING, db_column='materia_prima_codigo', null=True)
    quantidade = models.FloatField()
    unid_medida_codigo = models.ForeignKey('UnidMedida', models.DO_NOTHING, db_column='unid_medida_codigo', null=True)
    id = models.ForeignKey('Producao', on_delete=models.CASCADE, null=True, db_column='id')
    # producao_artesao_codigo = models.ForeignKey('Producao', models.DO_NOTHING, db_column='artesao_codigo', related_name='producao_artesao_codigo')
    # producao_tipo_prod_codigo = models.ForeignKey('Producao', models.DO_NOTHING, db_column='producao_tipo_prod_codigo', related_name='producao_tipo_prod_codigo')

    class Meta:
        managed = True
        db_table = 'mp_prod'

    def __str__(self):
        return f'{self.materia_prima_codigo} | Estoque: {self.quantidade} {self.unid_medida_codigo}'


# Classe tabela Produto Vendido
class ProdVendido(models.Model):
    codigo_venda = models.IntegerField(primary_key=True)
    data = models.DateField()
    local = models.CharField(max_length=10)
    preco_final = models.DecimalField(max_digits=6, decimal_places=2)
    produto_stock_tipo_prod_codigo = models.ForeignKey('ProdutoStock', models.DO_NOTHING, db_column='produto_stock_tipo_prod_codigo')

    class Meta:
        managed = True
        db_table = 'prod_vendido'

    def __str__(self):
        return f'{self.produto_stock_tipo_prod_codigo} | Preço Final: {self.preco_final}'


# Classe tabela Produção
class Producao(models.Model):
    # artesao_codigo = models.ForeignKey(Artesao, models.DO_NOTHING, db_column='artesao_codigo')
    # tipo_prod_codigo = models.OneToOneField('TipoProd', models.DO_NOTHING, db_column='tipo_prod_codigo')
    id = models.AutoField(primary_key=True, null=True, db_column='id')
    artesao_codigo = models.ForeignKey('Artesao', on_delete=models.CASCADE, null=True)
    tipo_prod_codigo = models.ForeignKey('TipoProd', on_delete=models.CASCADE, null=True)
    tempo_producao = models.IntegerField()
    custo_hora_producao = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'producao'
        # unique_together = (('artesao_codigo', 'tipo_prod_codigo'),)

    def __str__(self):
        return f'Prdução (ID: {self.id})'


# Classe tabela Produto em Stock
class ProdutoStock(models.Model):
    tipo_prod_codigo = models.OneToOneField('TipoProd', models.DO_NOTHING, db_column='tipo_prod_codigo', primary_key=True)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'produto_stock'

    def __str__(self):
        return f'{self.tipo_prod_codigo}'


# Classe tabela Tipode de Produto
class TipoProd(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(unique=True, max_length=50)
    imagem = models.ImageField(upload_to='images/produtos/')
    custo_producao = models.DecimalField(max_digits=6, decimal_places=2, null=True, default=0)
    lucro = models.FloatField()
    preco = models.DecimalField(max_digits=6, decimal_places=2, null=True, default=0)
    categoria_codigo = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='categoria_codigo')

    class Meta:
        managed = True
        db_table = 'tipo_prod'

    def __str__(self):
        return f'{self.nome}'


# Classe tabela Unidade de Medida
class UnidMedida(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=20, blank=True, null=True)
    abreviatura = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'unid_medida'

    def __str__(self):
        return f'{self.nome}' if self.abreviatura == '' else f'{self.nome} ({self.abreviatura})'
