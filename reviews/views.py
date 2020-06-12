from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice, Review, ReviewStatus
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

# Create your views here.


class AddReviewForm(generic.ListView):
    template_name = 'reviews/add_review_form.html'
    context_object_name = 'current_review'

    def get_queryset(self):
        """Return the last five published questions."""
        return Review.objects.order_by('id')


# @login_required(login_url='/admin/login/')
def add_review_action(request):
    try:
        if not request.user.is_authenticated:
            raise Exception('Not Auth')

        review_text = request.POST['review_text']
        r = Review()
        r.text = review_text
        r.status = ReviewStatus.objects.filter(name__startswith='MO')[0]
        r.created_at = timezone.now()
        r.changed_at = timezone.now()
        r.created_by = request.user
        r.changed_by = request.user
        r.save()
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'reviews/add_review_form.html', {
            'error_message': e.__str__(),
        })
    except Exception as e:
        return render(request, 'reviews/add_review_form.html', {
            'error_message': e.__str__(),
        })
    else:
        return HttpResponseRedirect(reverse('reviews:add_review_form'))


class IndexView(generic.ListView):
    template_name = 'reviews/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'reviews/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'reviews/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'reviews/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:results', args=(question.id,)))

