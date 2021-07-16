#  artgest/urls.py


from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static


app_name = "artgest"

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('sobre', views.sobre_page_view, name='sobre'),
    path('info', views.info_page_view, name='info'),
    path('userpage', views.userpage_page_view, name='userpage'),
    path('produtos_registar', views.registar_produtos_page_view, name='produtos_registar'),
    path('produtos_listar', views.listar_produtos_page_view, name='produtos_listar'),
    path('produtos_editar/<int:tipoprod_codigo>', views.editar_produtos_page_view, name='produtos_editar'),
    path('produtos_eliminar/<int:tipoprod_codigo>', views.eliminar_produtos_page_view, name='produtos_eliminar'),
    path('produtos_visualizar/<int:tipoprod_codigo>', views.visualizar_produtos_page_view, name='produtos_visualizar'),
    path('producao_eliminar/<int:tipoprod_codigo>', views.eliminar_producao_view, name='producao_eliminar'),
    path('materiasprimas_registar', views.registar_materiasprimas_page_view, name='materiasprimas_registar'),
    path('materiasprimas_listar', views.listar_materiasprimas_page_view, name='materiasprimas_listar'),
    path('materiasprimas_editar/<int:materia_prima_codigo>', views.editar_materiasprimas_page_view, name='materiasprimas_editar'),
    path('materiasprimas_eliminar/<int:materia_prima_codigo>', views.eliminar_materiasprimas_view, name='materiasprimas_eliminar'),
    path('gastos_registar', views.registar_gastos_page_view, name='gastos_registar'),
    path('gastos_listar', views.listar_gastos_page_view, name='gastos_listar'),
    path('gastos_editar/<int:gasto_codigo>', views.editar_gastos_page_view, name='gastos_editar'),
    path('gastos_eliminar/<int:gasto_codigo>', views.eliminar_gastos_view, name='gastos_eliminar'),
    path('fornecedores_registar', views.registar_fornecedores_page_view, name='fornecedores_registar'),
    path('fornecedores_listar', views.listar_fornecedores_page_view, name='fornecedores_listar'),
    path('fornecedores_editar/<str:fornecedor_nipc>', views.editar_fornecedores_page_view, name='fornecedores_editar'),
    path('fornecedores_eliminar/<str:fornecedor_nipc>', views.eliminar_fornecedores_view, name='fornecedores_eliminar'),
    path('instrucoes_registar', views.registar_instrucoes_page_view, name='instrucoes_registar'),
    path('instrucoes_listar', views.listar_instrucoes_page_view, name='instrucoes_listar'),
    path('instrucoes_editar/<int:instrucao_codigo>', views.editar_instrucoes_page_view, name='instrucoes_editar'),
    path('instrucoes_eliminar/<int:instrucao_codigo>', views.eliminar_instrucoes_view, name='instrucoes_eliminar'),
    path('prodvendidos_registar', views.registar_prodvendidos_page_view, name='prodvendidos_registar'),
    path('prodvendidos_listar', views.listar_prodvendidos_page_view, name='prodvendidos_listar'),
    path('prodvendidos_editar/<int:pv_codigo_venda>', views.editar_prodvendidos_page_view, name='prodvendidos_editar'),
    path('prodvendidos_eliminar/<int:pv_codigo_venda>', views.eliminar_prodvendidos_view, name='prodvendidos_eliminar'),
    path('relatorios', views.relatorios_page_view, name='relatorios'),
    path('alertas', views.alertas_page_view, name='alertas'),
    path('limpa_alerta/<int:alerta_codigo>', views.limpa_alerta_page_view, name='limpa_alerta'),
    path('perfil/<int:artesao_codigo>', views.perfil_page_view, name='perfil'),
    path('perfil_visualizar/<int:artesao_codigo>', views.perfil_visualizar_page_view, name='perfil_visualizar'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)