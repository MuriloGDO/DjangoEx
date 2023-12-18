from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('dologin/', include('main.urls')),
    path('dashboard_projetos/', include('main.urls')),
    path('logouts/', include('main.urls')),
    path('inicio/', include('main.urls')),
    path('dashboard_projetos_empresa/', include('main.urls')),
    path('gerenciar/', include('main.urls')),
    path('ad_perm/', include('main.urls')),
    path('ad_empresa/', include('main.urls')),
    path('rem_empresa/', include('main.urls')),
    path('ad_proj/', include('main.urls')),
    path('rem_proj/', include('main.urls')),
    path('ad_pes/', include('main.urls')),
    path('rem_pes/', include('main.urls')),
    path('perm/', include('main.urls')),
    path('empresa_ad/', include('main.urls')),
    path('empresa_rem/', include('main.urls')),
    path('proj_ad/', include('main.urls')),
    path('proj_proj/', include('main.urls')),
    path('pes_ad/', include('main.urls')),
    path('pes_rem/', include('main.urls')),
    path('list/', include('main.urls')),
    path('list_pes/', include('main.urls')),
]
