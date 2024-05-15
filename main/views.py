from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Empresa, Projetos, UserProjetosEmpresa, Permissao
from django.db.models import Q

# Criando os usuários
def one_time():
    if not User.objects.filter(username='user1').exists():
        user1 = User.objects.create_user(username='user1', password='senha_caso1')
        user1.save()
    if not User.objects.filter(username='user2').exists():
        user2 = User.objects.create_user(username='user2', password='senha_caso2')
        user2.save()
    if not User.objects.filter(username='user3').exists():
        user3 = User.objects.create_user(username='user3', password='senha_caso3')
        user3.save()
    if not User.objects.filter(username='user4').exists():
        user4 = User.objects.create_user(username='user4', password='senha_caso4')
        user4.save()

# Create your views here.
def tela_de_login(request):
    one_time()
    return render(request, 'index.html')

#Processar Login
def dologin(request):
    if not User.objects.filter(username=request.POST['usuario']).exists():
        return render(request, 'erro_usuario.html')
    user = authenticate(username=request.POST['usuario'], password=request.POST['senha'])
    if user is not None:
        login(request, user)
        return redirect('/inicio/')
    else:
        return render(request, 'erro_senha.html')

def dashboard_projetos(request):
    user = request.user
    try:
        dono_projetos = Projetos.objects.filter(admin_proj = user.id)
        projetos_relacionados = UserProjetosEmpresa.objects.filter(cod_user = user.id)
        projetos_ids = projetos_relacionados.values_list('cod_projeto', flat=True)
        projetos = Projetos.objects.filter(id__in=projetos_ids)
        projetos = projetos.exclude(id__in=dono_projetos.values_list('id', flat=True))
        return render(request, 'dashboard_projetos.html', {'projetos' : projetos, 'dono_projetos' : dono_projetos})
    except UserProjetosEmpresa.DoesNotExist:
        return HttpResponse("Erro")

def logouts(request):
    logout(request)
    return redirect('/')

def inicio(request):
    user = request.user
    try:
        aux = UserProjetosEmpresa.objects.filter(cod_user = user.id)
        dono_empresa = Empresa.objects.filter(admin_emp = user.id)
        empresas_ids = aux.values_list('cod_empresa', flat=True)
        empresas_user = Empresa.objects.filter(id__in = empresas_ids)
        empresas_user = empresas_user.exclude(id__in=dono_empresa.values_list('id', flat=True))
        return render(request, 'dashboard_inicio.html', {'empresas_user' : empresas_user, 'dono_empresa' : dono_empresa })
    except UserProjetosEmpresa.DoesNotExist:
        return HttpResponse("Erro")

def dashboard_projetos_empresa(request):
    parametro1 = request.GET.get('parametro1')
    user = request.user
    try:
        projetos_empresa = UserProjetosEmpresa.objects.filter(cod_user = user.id,cod_empresa = parametro1)
        projetos_ids = projetos_empresa.values_list('cod_projeto', flat=True)
        projetos = Projetos.objects.filter(id__in=projetos_ids)
        return render(request, 'dashboard_projetos.html', {'projetos' : projetos})
    except UserProjetosEmpresa.DoesNotExist:
        return HttpResponse("Erro")

def gerenciar(request):
    return render(request, 'gerenciar.html')

def ad_perm(request):
    valor = 'ad_perm'
    return render(request, 'gerenciar.html', {'valor' : valor})

def ad_empresa(request):
    valor = 'ad_empresa'
    return render(request, 'gerenciar.html', {'valor' : valor})

def rem_empresa(request):
    valor = 'rem_empresa'
    return render(request, 'gerenciar.html', {'valor' : valor})

def ad_proj(request):
    valor = 'ad_proj'
    return render(request, 'gerenciar.html', {'valor' : valor})

def rem_proj(request):
    valor = 'rem_proj'
    return render(request, 'gerenciar.html', {'valor' : valor})

def ad_pes(request):
    valor = 'ad_pes'
    return render(request, 'gerenciar.html', {'valor' : valor})

def rem_pes(request):
    valor = 'rem_pes'
    return render(request, 'gerenciar.html', {'valor' : valor})

def list(request):
    valor = 'list'
    return render(request, 'gerenciar.html', {'valor' : valor})

def perm(request):
    if request.method == 'POST':
        user = request.user
        usuario_nome = request.POST.get('usuario', '')
        usuario = User.objects.get(username = usuario_nome)
        empresa_nome = request.POST.get('empresa', '')  
        try:
            empresa = Empresa.objects.get(nome=empresa_nome, admin_emp=user.id)
        except Empresa.DoesNotExist:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})

        
        if Permissao.objects.filter(cod_user=usuario, cod_empresa=empresa).exists():
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
        else:
            
            nova_permissao = Permissao.objects.create(cod_user=usuario, cod_empresa=empresa)
            nova_permissao.save()

            concluido = 1
            return render(request, 'gerenciar.html', {'concluido': concluido})
    else:
        erro = 1
        return render(request, 'gerenciar.html', {'erro': erro})
   

def empresa_ad(request):
    if request.method == 'POST':
        user = request.user
        empresa_nome = request.POST.get('empresa', '')
        desc_n = request.POST.get('desc', '')

        try:
            
            empresa_existente = Empresa.objects.filter(nome=empresa_nome, admin_emp=user)
            
            if empresa_existente.exists():
                erro = 1
                return render(request, 'gerenciar.html', {'erro': erro})
            
            
            nova_empresa = Empresa(nome=empresa_nome, desc=desc_n, admin_emp=user)
            nova_empresa.save()

            
            permissao = Permissao(cod_user=user, cod_empresa=nova_empresa)
            permissao.save()

            concluido = 1
            return render(request, 'gerenciar.html', {'concluido': concluido})
        
        except Exception as e:
            
            print(f"Erro: {e}")
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
    else:
        erro = 1
        return render(request, 'gerenciar.html', {'erro': erro})
   
def empresa_rem(request):
    if request.method == 'POST':
        user = request.user
        empresa_nome = request.POST.get('empresa', '')

        try:
            
            empresa_para_excluir = Empresa.objects.get(nome=empresa_nome, admin_emp=user.id)
            
            
            projetos_relacionados = UserProjetosEmpresa.objects.filter(cod_empresa = empresa_para_excluir.id)
            projetos_ids = projetos_relacionados.values_list('cod_projeto', flat=True)
            projetos_para_excluir = Projetos.objects.filter(id__in=projetos_ids)

            if projetos_relacionados:
                projetos_relacionados.delete()
            if projetos_para_excluir:
                projetos_para_excluir.delete()

            
            empresa_para_excluir.delete()

            concluido = 1
            return render(request, 'gerenciar.html', {'concluido': concluido})
        except Empresa.DoesNotExist:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
        except Exception:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
    else:
        erro = 1
        return render(request, 'gerenciar.html', {'erro': erro})
    
def proj_ad(request):
    if request.method == 'POST':
        user = request.user
        projeto_nome = request.POST.get('projeto_nome', '')
        empresa_nome = request.POST.get('empresa', '')
        dono_empresa = request.POST.get('dono_empresa', '')
        desc_n = request.POST.get('desc', '')
        dono_id = User.objects.get(username = dono_empresa)

        try:
            
            empresa_obj = Empresa.objects.get(nome=empresa_nome, admin_emp = dono_id.id)
            
            
            if not Permissao.objects.filter(cod_empresa=empresa_obj.id, cod_user=user.id).exists():
                erro = 1
                return render(request, 'gerenciar.html', {'erro': erro})

            
            if Projetos.objects.filter(nome=projeto_nome, admin_proj=user.id).exists():
                erro = 1
                return render(request, 'gerenciar.html', {'erro': erro})
            
            
            novo_projeto = Projetos(nome=projeto_nome, desc=desc_n, admin_proj=user)
            novo_projeto.save()

            
            nova_relacao = UserProjetosEmpresa(cod_user=user, cod_projeto=novo_projeto, cod_empresa=empresa_obj)
            nova_relacao.save()
            
            concluido = 1
            return render(request, 'gerenciar.html', {'concluido': concluido})

        except Empresa.DoesNotExist:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
    
    else:
        erro = 1
        return render(request, 'gerenciar.html', {'erro': erro})
    

def proj_rem(request):
    if request.method == 'POST':
        user = request.user
        projeto_nome = request.POST.get('projeto', '')

        try:
            projeto_para_excluir = Projetos.objects.get(nome=projeto_nome, admin_proj=user.id)
            projeto_para_excluir.delete()

            concluido = 1
            return render(request, 'gerenciar.html', {'concluido': concluido})
        except Projetos.DoesNotExist:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
        except Exception:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
    else:
        erro = 1
        return render(request, 'gerenciar.html', {'erro': erro})



def pes_ad(request):
    user = request.user
    projeto = request.POST.get('projeto', '')
    usuario_add = request.POST.get('usuario', '')
    empresa_add = request.POST.get('empresa', '')

    
    empresa_obj = Empresa.objects.get(nome=empresa_add)
    usuario_obj = User.objects.get(username=usuario_add)

    verifica = Projetos.objects.get(nome=projeto, admin_proj=user.id)
    
   
    if verifica and empresa_obj and usuario_obj:
        novo_objeto = UserProjetosEmpresa(cod_user=usuario_obj, cod_projeto=verifica, cod_empresa=empresa_obj)
        novo_objeto.save()
        concluido = 1
        return render(request, 'gerenciar.html', {'concluido': concluido})
    else:
        erro = 1
        return render(request, 'gerenciar.html', {'erro': erro})


def pes_rem(request):
    user = request.user
    usuario_nome = request.POST.get('usuario', '')
    empresa_nome = request.POST.get('empresa', '')
    usuario_obj = User.objects.get(username=usuario_nome)
    empresa = Empresa.objects.get(nome= empresa_nome)
    projeto = request.POST.get('projeto', '')
    projeto_obj = Projetos.objects.get(nome=projeto, admin_proj=user.id)

    try: 
        if projeto_obj:
            
            user_projeto_empresa_obj = UserProjetosEmpresa.objects.get(cod_user=usuario_obj.id, cod_projeto=projeto_obj.id, cod_empresa=empresa.id)
            
            
            if user_projeto_empresa_obj:
                user_projeto_empresa_obj.delete()
                concluido = 1
                return render(request, 'gerenciar.html', {'concluido': concluido})
            else:
                erro = 1
                return render(request, 'gerenciar.html', {'erro': erro})
        else:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
    except Exception:
            erro = 1
            return render(request, 'gerenciar.html', {'erro': erro})
    
