from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Alerta)
admin.site.register(Artesao)
admin.site.register(Categoria)
admin.site.register(Fornecedor)
admin.site.register(Fornecimento)
admin.site.register(Gastos)
admin.site.register(GastosProd)
admin.site.register(InstProd)
admin.site.register(Instrucoes)
admin.site.register(MateriaPrima)
admin.site.register(MpProd)
admin.site.register(Producao)
admin.site.register(ProdutoStock)
admin.site.register(ProdVendido)
admin.site.register(TipoProd)
admin.site.register(UnidMedida)
