from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=30)
    desc = models.TextField() 
    admin_emp = models.ForeignKey(User, on_delete=models.CASCADE)

class Projetos(models.Model):
    nome = models.CharField(max_length=30)
    desc = models.TextField()
    admin_proj = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProjetosEmpresa(models.Model):
    cod_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cod_projeto = models.ForeignKey(Projetos, on_delete=models.CASCADE)
    cod_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class Permissao(models.Model):
    cod_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cod_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)