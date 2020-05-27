# realiza los templates de forma automatica, entrega un error 404 cuando no encuentra la encuesta
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import Question, Choise
# from django.template import loader # cuando se usa HttpResponse y un template

# Create your views here.


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #template = loader.get_template('encuestas/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'encuestas/index.html', context)


def detail(request, question_id):
    # return HttpResponse("You're looking at quiestion %s." % question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    # return render(request, 'polls/detail.html', {'question': question}) #Usar si se utiliza Http404
    question = get_object_or_404(Question, pk=question_id)
    # usando get_object_or_404
    return render(request, 'encuestas/detail.html', {'question': question})


def results(request, question_id):
    #response = "You're looking at the result of %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'encuestas/results.html', {'question': question})


def vote(request, question_id):
    # Dummy implementation
    # return HttpResponse("You're voting on question %s." % question_id)

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choise_set.get(pk=request.POST['choice'])
    except (KeyError, Choise.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'encuestas/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # F permite que no se realicen race-conditions entre otras cosas. Trabaja directo con la base db
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
