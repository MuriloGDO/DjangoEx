from django.urls import path
from . import views

urlpatterns = [
    path('', views.tela_de_login, name="tela_de_login"),
    path('dologin/', views.dologin, name="dologin"),
    path('dashboard_projetos/', views.dashboard_projetos, name="dashboard_projetos"),
    path('logouts/', views.logouts, name="logouts"),
    path('inicio/', views.inicio, name="inicio"),
    path('dashboard_projetos_empresa/', views.dashboard_projetos_empresa, name="dashboard_projetos_empresa"),
    path('gerenciar/', views.gerenciar, name="gerenciar"),
    path('ad_perm/', views.ad_perm, name="ad_perm"),
    path('ad_empresa/', views.ad_empresa, name="ad_empresa"),
    path('rem_empresa/', views.rem_empresa, name="rem_empresa"),
    path('ad_proj/', views.ad_proj, name="ad_proj"),
    path('rem_proj/', views.rem_proj, name="rem_proj"),
    path('ad_pes/', views.ad_pes, name="ad_pes"),
    path('rem_pes/', views.rem_pes, name="rem_pes"),
    path('perm/', views.perm, name="perm"),
    path('empresa_ad/', views.empresa_ad, name="empresa_ad"),
    path('empresa_rem/', views.empresa_rem, name="empresa_rem"),
    path('proj_ad/', views.proj_ad, name="proj_ad"),
    path('proj_rem/', views.proj_rem, name="proj_rem"),
    path('pes_ad/', views.pes_ad, name="pes_ad"),
    path('pes_rem/', views.pes_rem, name="pes_rem"),
    path('list/', views.list, name="list"),
    path('list_pes/', views.list_pes, name="list_pes"),
]