from django.contrib import admin
from credito.models import Compras, DataPagamento


class ComprasAdmin(admin.ModelAdmin):

    list_display = ['id', 'data_pagamento', 'data_compra', 'loja', 'valor', 'descricao', 'responsavel']
    search_fields = ['loja', 'descricao', 'responsavel']
    list_filter = ['data_pagamento']

    def get_ordering(self, request):
        return ['-data_pagamento']


admin.site.register(Compras, ComprasAdmin)
admin.site.register(DataPagamento)
