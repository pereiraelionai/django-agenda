from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):

    # contatos_bd = Contato.objects.all()
    contatos_bd = Contato.objects.order_by('-id') # adicionando um sinal de - ele ordena por ordem decrescente
    # contatos_bd = Contato.objects.order_by('-id').filter(
    #     mostrar=True
    # ) # Outra maneira de fazer um filtro, nesse momento estou utilizando if no index.html

    paginator = Paginator(contatos_bd, 5)

    page = request.GET.get('p')
    contatos_bd = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'chave_contatos': contatos_bd
    })

'''
def ver_contato(request, contato_id): # contato id veio do urls (<int:contato_id>)
    try:
        contato = Contato.objects.get(id=contato_id)
        return render(request, 'contatos/ver_contato.html', {
            'contato': contato
        })
    except Contato.DoesNotExist as erro:
        raise Http404()
'''


def ver_contato(request, contato_id): # contato id veio do urls (<int:contato_id>)
    # contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        # raise Http404()
        messages.add_message(request, messages.ERROR, 'Campo pesquisa não pode estar vazio.')
        return redirect('index')

    campos = Concat('nome', Value(' '),  'sobrenome')

    contatos_bd = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) |
        Q(telefone__icontains=termo)
    )

    '''
    contatos_bd = Contato.objects.order_by('-id').filter(
        Q(nome__icontains=termo) |
        Q(sobrenome__icontains=termo)
    )
    '''

    # print(contatos_bd.query)

    paginator = Paginator(contatos_bd, 5)

    page = request.GET.get('p')
    contatos_bd = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'chave_contatos': contatos_bd
    })
