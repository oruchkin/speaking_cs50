from django.shortcuts import render
from .models import Reputation, User, Theme, Question, Audio_answer
from .utils import member_for, get_user


def profile(request, user_pk):
    target_user = User.objects.get(pk=user_pk)
    #hide hidden answers
    if get_user(request) == target_user:
        users_answers = Audio_answer.objects.filter(author=target_user).order_by("-pk")
    else:
        users_answers = Audio_answer.objects.filter(author=target_user, share_answer=True).order_by("-pk")
    users_questions = Question.objects.filter(author=target_user).order_by("-pk")[0:5]
    users_themes = Theme.objects.filter(author=target_user).order_by("-pk")[0:5]
    users_reputation = Reputation.objects.filter(reciever=target_user).order_by('-pk')[0:5]

    counter = {"reputation":target_user.reputation,
        "answers_counter": len(users_answers),
        "question_counter": len(Question.objects.filter(author=target_user)),
        "theme_counter": len(Theme.objects.filter(author=target_user)),
        "reputation_counter": len(Reputation.objects.filter(reciever=target_user))}
    
    context = {"target_user":target_user,
               "users_answers":users_answers[0:5],
               "users_questions":users_questions,
               "users_themes":users_themes,
               "users_reputation":users_reputation,
               "member":member_for(target_user.date_joined),
               "counter":counter}
    
    return render(request, 'spapp/profile/profile.html', context)    


def profile_answers(request,user_pk):
    target_user = User.objects.get(pk=user_pk)
    #hide hidden answers
    if get_user(request) == target_user:
        users_answers = Audio_answer.objects.filter(author=target_user).order_by("-pk")
    else:
        users_answers = Audio_answer.objects.filter(author=target_user, share_answer=True).order_by("-pk")
    
    counter = {"reputation":target_user.reputation,
        "answers_counter": len(users_answers),
        "question_counter": len(Question.objects.filter(author=target_user)),
        "theme_counter": len(Theme.objects.filter(author=target_user))}
    
    context = {"target_user":target_user,
               "users_answers":users_answers,
               "member":member_for(target_user.date_joined),
               "counter":counter}
    
    return render(request, 'spapp/profile/profile_answers.html', context)    
        
        
def profile_questions(request,user_pk):
    target_user = User.objects.get(pk=user_pk)
    if get_user(request) == target_user:
        users_answers = Audio_answer.objects.filter(author=target_user).order_by("-pk")
    else:
        users_answers = Audio_answer.objects.filter(author=target_user, share_answer=True).order_by("-pk")
    users_questions = Question.objects.filter(author=target_user).order_by("-pk")
    counter = {"reputation":target_user.reputation,
        "answers_counter": len(users_answers),
        "question_counter": len(Question.objects.filter(author=target_user)),
        "theme_counter": len(Theme.objects.filter(author=target_user))}
    
    context = {"target_user":target_user,
               "users_questions":users_questions,
               "member":member_for(target_user.date_joined),
               "counter":counter}
    
    return render(request, 'spapp/profile/profile_questions.html', context)    


def profile_theme(request,user_pk):
    target_user = User.objects.get(pk=user_pk)
    if get_user(request) == target_user:
        users_answers = Audio_answer.objects.filter(author=target_user).order_by("-pk")
    else:
        users_answers = Audio_answer.objects.filter(author=target_user, share_answer=True).order_by("-pk")
    users_themes = Theme.objects.filter(author=target_user).order_by("-pk")
    counter = {"reputation":target_user.reputation,
        "answers_counter": len(users_answers),
        "question_counter": len(Question.objects.filter(author=target_user)),
        "theme_counter": len(Theme.objects.filter(author=target_user))}
    
    context = {"target_user":target_user,
               "users_themes":users_themes,
               "member":member_for(target_user.date_joined),
               "counter":counter}
    return render(request, 'spapp/profile/profile_themes.html', context)    
        

def profile_reputation(request,user_pk):
    target_user = User.objects.get(pk=user_pk)
    if get_user(request) == target_user:
        users_answers = Audio_answer.objects.filter(author=target_user).order_by("-pk")
    else:
        users_answers = Audio_answer.objects.filter(author=target_user, share_answer=True).order_by("-pk")
    users_reputations = Reputation.objects.filter(reciever=target_user).order_by("-pk")
    counter = {"reputation":target_user.reputation,
        "answers_counter": len(users_answers),
        "question_counter": len(Question.objects.filter(author=target_user)),
        "theme_counter": len(Theme.objects.filter(author=target_user)),
        "reputation_counter": len(users_reputations)}
    
    context = {"target_user":target_user,
               "users_reputations":users_reputations,
               "member":member_for(target_user.date_joined),
               "counter":counter}
    return render(request, 'spapp/profile/profile_reputation.html', context)    