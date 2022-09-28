from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question
from django.utils import timezone
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import  messages


@login_required(login_url='common:login')
def question_create(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', {'form':form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk = question_id)

    if request.user != question.author:
        messages.error(request,'수정권한이 없습니다')
        return redirect('pybo:detail',question_id = question.id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail',question_id = question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(reqeust, question_id):
    question= get_object_or_404(Question, pk = question_id)
    if reqeust.user != question.author:
        messages.error(reqeust, "삭제 권한이 없습니다.")
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')