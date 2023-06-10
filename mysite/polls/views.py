from django.http import HttpResponse, HttpResponseRedirect
# using templates so we need the following:
from django.template import loader
from django.shortcuts import get_object_or_404, render
# 404
from django.http import Http404
from django.utils import timezone


# for our vote def
from django.urls import reverse
from django.views import generic

# we are using the models in this file so we need to import them
from .models import Choice, Question

class IndexView(generic.ListView):
    #return HttpResponse("Hello, world. You're at the polls index. Updated")
    # step 1 - gather the data
    #latest_question_list = Question.objects.order_by("-pub_date")[:5] 
    # step 2 - assign a template
    #template = loader.get_template("polls/index.html")
    #context = { 
    #   "latest_question_list": latest_question_list,     
    #}
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    #output = ", ".join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    #return HttpResponse(template.render(context, request))
    #return render(request, "polls/index.html", context)
    # Refactored:
    # The render() function takes the request object as its first argument, 
    # a template name as its second argument and a dictionary as its optional 
    # third argument. It returns an HttpResponse object of the given 
    # template rendered with the given context.

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"   
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, "polls/detail.html", {"question": question})
    #def detail(request, question_id):
    # non logic version
    # return HttpResponse("You're looking at question %s." % question_id)
    # new logic w/ 404 check
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Quesiton does not exist")
    #return render(request, "polls/detail.html", {"question": question})
    # new logic using get_object_or_404()


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    #def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    # stub
    #return HttpResponse("You're voting on qustion %s." % question_id)
    # lesson 4
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    # The code enters the else block only if the try clause does not raise an exception.
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
