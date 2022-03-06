from django.shortcuts import render, redirect
from credito.models import Compras
import datetime
import requests
from json import dumps


mes_english = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
               'October', 'November', 'December']

mes_port = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO',
               'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

TODAY = datetime.date.today()
ultimo = datetime.datetime(TODAY.year, TODAY.month, 1)
MES_ATUAL = str(TODAY.strftime("%B"))
MES_ATUAL_INDEX = mes_english.index(MES_ATUAL)
MES_ATUAL_PT = mes_port[MES_ATUAL_INDEX]
PROX_MES = mes_english[MES_ATUAL_INDEX + 1]
first = TODAY.replace(day=1)
lastday = first - datetime.timedelta(days=1)

def penultimate_day_of_month(date):
    if date.month == 12:
        return date.replace(day=30)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=2)


def next_payday(date):
    if date < penultimate_day_of_month(date):
        if date.month >= 12:
            return date.replace(year=date.year + 1, month=1, day=9)
        return date.replace(month=date.month + 1, day=9)
    else:
        data_payday = date.replace(month=date.month+2, day=9)
        return data_payday


def mes_referencia(date):
    mes_ref = str(date.strftime("%B"))
    mes_ref_index = mes_english.index(mes_ref)
    mes_ref_pt = mes_port[mes_ref_index]
    return mes_ref_pt


def fatura(request):
    context = {}
    data_pagamento = next_payday(TODAY)
    compras = Compras.objects.filter(data_pagamento=data_pagamento).order_by('data_compra')
    valor_total = Compras.objects.filter(data_pagamento=data_pagamento)
    valor_total_credito  = Compras.objects.filter(data_pagamento=data_pagamento).filter(parcela__icontains="/")
    valor_total_externo = Compras.objects.filter(data_pagamento=data_pagamento).filter(categoria="EXTERNO")

    soma_compras = 0
    for t in valor_total:
        valort = t.valor.replace(',','.')
        soma_compras += float(valort)

    soma_credito = 0
    for v in valor_total_credito:
       valor = v.valor.replace(',','.')
       soma_credito += float(valor)

    soma_externo = 0
    for e in valor_total_externo:
       valor = e.valor.replace(',','.')
       soma_externo  += float(valor)

    context['VALOR_TOTAL_CREDITO'] = '{:.2f}'.format(soma_credito)
    context['VALOR_TOTAL_EXTERNO'] = '{:.2f}'.format(soma_externo)
    context['VALOR_A_PAGAR'] = '{:.2f}'.format(soma_compras - soma_externo)
    context['VENCIMENTO'] = data_pagamento
    context['VALOR_TOTAL'] = '{:.2f}'.format(soma_compras)
    context['compras'] = compras
    #context['contador'] = [x for x in range(1, compras.count() + 1)]
    context['MES_REFERENCIA'] = mes_referencia(next_payday(TODAY)).capitalize()

    return render(request, 'credito/fatura.html', context)


def add_compra(request):
    context = {}
    data_pagamento = next_payday(TODAY)

    if request.method == "POST":
        compras = dict(request.POST.items())
        data_pagamento = datetime.datetime.strptime(compras['data_pagamento'], "%d/%m/%Y")
        data_compra = datetime.datetime.strptime(compras['data_compra'], "%d/%m/%Y")
        new_payday = next_payday(data_compra).date()
        if '/' in compras['parcelas']:
            parcelas = compras['parcelas'].split("/")

            for n in range(1, int(parcelas[1]) +1 ):
                parcela = f'{n}/{int(parcelas[1])}'

                if new_payday.month + n - 1 > 12:
                    mes = new_payday.month + n - 13
                    ano = new_payday.year + 1
                else:
                    mes = new_payday.month + n -1
                    ano = new_payday.year

                add_payday = new_payday.replace(year=ano, month=mes, day=9)
                #print(data_compra.date(), add_payday, parcela, compras['loja'])
                nova_compra = Compras.objects.create(data_pagamento=add_payday, data_compra=data_compra.date(),
                                                     loja=compras['loja'], parcela=parcela,
                                                     valor=compras['valor'],
                                                     descricao=compras['descricao'], categoria=compras['categoria'],
                                                     responsavel=compras['responsavel'])
                nova_compra.save()
        else:
            nova_compra = Compras.objects.create(data_pagamento=data_pagamento, data_compra=data_compra,
                                                 loja=compras['loja'], parcela=compras['parcelas'], valor=compras['valor'],
                                                 descricao=compras['descricao'], categoria=compras['categoria'],
                                                 responsavel=compras['responsavel'])
            nova_compra.save()

        if "continue" in compras:
            return redirect('add_compra')
        elif "save" in compras:
            return redirect('fatura')

    return render(request, 'credito/add_compra.html', context)


def edit_compra(request, pk):
    context = {}
    data_pagamento = next_payday(TODAY)
    compra = Compras.objects.get(pk=pk)

    if request.method == "POST":
        compras = dict(request.POST.items())
        data_pagamento = datetime.datetime.strptime(compras['data_pagamento'], "%d/%m/%Y")
        data_compra= datetime.datetime.strptime(compras['data_compra'], "%d/%m/%Y")

        compra.data_pagamento=data_pagamento
        compra.data_compra=data_compra
        compra.loja=compras['loja']
        compra.parcela=compras['parcelas']
        compra.valor=compras['valor']
        compra.descricao=compras['descricao']
        compra.categoria=compras['categoria']
        compra.responsavel=compras['responsavel']

        compra.save()
        return redirect('fatura')

    return render(request, 'credito/edit_compra.html', context)


def del_compra(request, pk):

    compra = Compras.objects.get(pk=pk)
    compra.delete()

    return redirect('fatura')


def TransDatas():
    link = 'https://contas-diogoigarassu.herokuapp.com/credito/'
    data_pagamento = next_payday(TODAY)
    compras = Compras.objects.filter(data_pagamento=data_pagamento).order_by('data_compra')
    for compra in compras:
        data_pag = str(compra.data_pagamento.strftime('%Y-%m-%d'))
        data_comp = str(compra.data_compra.strftime('%Y-%m-%d'))
        print(data_comp, data_pag, compra.descricao)
        response = requests.post(link, auth=('admin','admin'), json={
          "data_pagamento": data_pag,
          "data_compra": data_comp,
          "loja": compra.loja,
          "parcela": compra.parcela,
          "valor": compra.valor,
          "descricao": compra.descricao,
          "categoria": compra.categoria,
          "responsavel": compra.responsavel
        })
        print(response.status_code)
    return print("Processo concluído!!!")
