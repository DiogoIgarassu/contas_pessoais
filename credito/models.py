from django.db import models

# Create your models here.
class Compras(models.Model):
    data_pagamento = models.DateField('Data de Pagamento', null=True, blank=True)
    data_compra = models.DateField('Data da Compra', null=True, blank=True)
    loja = models.CharField('Loja', max_length=100, null=True, blank=True)
    parcela = models.CharField('Parcela', max_length=5, null=True, blank=True)
    valor = models.CharField('Valor', max_length=7, null=True, blank=True)
    descricao = models.CharField('Descrição', max_length=100, null=True, blank=True)
    categoria = models.CharField('Categoria', max_length=100, null=True, blank=True)
    responsavel = models.CharField('Responsável', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'