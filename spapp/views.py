from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from .models import Theme, Question, Audio_answer
from .forms import New_theme_form 


def index(request):
    if request.method == "GET":
        context = {
            "all_themes":Theme.objects.all().order_by("-vote_count","pk"),
            "new_theme_form": New_theme_form(),
            "delete_theme_title":request.GET.get("delete_theme_title")
        }
        return render(request, 'spapp/index.html',context)    
    #new theme
    elif request.method == "POST":
        theme_form = New_theme_form(request.POST, request.FILES)
        if theme_form.is_valid():
            user = request.user
            title = theme_form.cleaned_data['title']
            target_image = theme_form.cleaned_data['image']
            new_theme = Theme(author = user, title=title, image = target_image)
            new_theme.save()
            return HttpResponseRedirect(reverse("theme_detailed",args=[new_theme.slug]))
        else:
            return HttpResponseRedirect(reverse("index"))


def new_audio_answer(request, q_slug):
    if request.method == "GET":
        question_obj = Question.objects.get(slug=q_slug)
        user = request.user
        return render(request, 'spapp/new_audio_answer.html',{
            "question_obj":question_obj,
            "user":user,
        })    
        

def delete_answer(request, answer_pk):
    if request.method == "GET":
        answer = Audio_answer.objects.get(pk=answer_pk)
        question = answer.question
        answer_pk = answer.pk
        answer.delete()
        return HttpResponseRedirect(reverse("question_detailed", \
            args=[question.slug]) + f'?ans_pk={answer_pk}&del=1')



