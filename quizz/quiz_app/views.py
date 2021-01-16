from django.shortcuts import render, redirect

from quizz.quiz_app.forms import AlunoForm
from quizz.quiz_app.models import Pergunta, Aluno


def verificar_se_aluno_existe_no_bd(request):
    '''
    Verificar se aluno já existe no BD
    :param request: requisição HTTP
    :return: Aluno
    '''
    email = request.POST['email']
    aluno = Aluno.objects.get(email=email)
    if aluno:
        return aluno

def validar_formulario_aluno(request):
    '''Validar formulário

    :param request:
    :return: redirect('/perguntas/1') or render for index
    '''
    form = AlunoForm(request.POST)
    if form.is_valid():
        # salvar aluno no BD e redirecionar para o quiz
        aluno = form.save()
        request.session['aluno_id'] = aluno.id
        return redirect('/perguntas/1')
    else:
        contexto = {'form': form}
        return render(request, 'quiz_app/index.html', contexto)

def index(request):
    if request.method == 'POST':
        try:
            aluno: Aluno = verificar_se_aluno_existe_no_bd(request)
        except Aluno.DoesNotExist:
            validar_formulario_aluno(request)
        else:
            request.session['aluno_id'] = aluno.id
            return redirect('/perguntas/1')

    return render(request, 'quiz_app/index.html')

def perguntas(request, indice: int):
    aluno_id = request.session['aluno_id']
    try:
        pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]

    except IndexError:
        return redirect('/classificacao')

    else:
        contexto = {
            'indice': indice,
            'pergunta': pergunta,
        }

        if request.method == 'POST':
            alternativa_escolhida = int(request.POST['alternativa'])

            if alternativa_escolhida - 1 == pergunta.alternativa_correta:
                return redirect(f'/perguntas/{indice + 1}')

            contexto['alternativa_escolhida'] = alternativa_escolhida

        return render(request, 'quiz_app/perguntas.html', contexto)

def classificacao(request):
    return render(request, 'quiz_app/classificacao.html')

