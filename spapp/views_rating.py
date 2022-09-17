from django.core.paginator import Paginator
from django.shortcuts import render
from .models import User, Theme, Question, Audio_answer
from .dataclass import User_rating,Theme_rating,Question_rating,Answer_rating
import hashlib
from django.db.models import Sum
from .utils import get_user

def rating_user(request):
    if request.method == "GET":
        logined_user = get_user(request)

            
        user_rating = []
        all_users = User.objects.all().order_by("-reputation")
        
        if logined_user:
            users_ids = list(all_users.values_list('id', flat= True))
            logined_user_rank = users_ids.index(logined_user.pk)+1
            size=30
            hash = (hashlib.md5(logined_user.email.encode('utf-8').lower()).hexdigest())
            img_result = f"https://www.gravatar.com/avatar/{hash}?s={size}&d=identicon&r=PG" 
            logined_user_obj = User_rating(pk = logined_user.pk,
                                            position = logined_user_rank,
                                            username = logined_user.username,
                                            reputation = logined_user.reputation,
                                            image_link = img_result)
        else: logined_user_obj = None
        paginator = Paginator(all_users, 25) 
        page_number = request.GET.get('page')
        paginated_users = paginator.get_page(page_number)
        counter = 0
        for user in paginated_users:
            counter += 1
            size=30
            hash = (hashlib.md5(user.email.encode('utf-8').lower()).hexdigest())
            img_result = f"https://www.gravatar.com/avatar/{hash}?s={size}&d=identicon&r=PG" 
            user_rating.append(User_rating(pk = user.pk,
                                            position = counter,
                                            username = user.username,
                                            reputation = user.reputation,
                                            image_link = img_result))
        context = {
            "all_users":user_rating,
            "page_obj":paginated_users,
            "logined_user_obj":logined_user_obj,
        }
        return render(request, 'spapp/rating/rating_user.html', context)    
    
    
    
def rating_theme(request):
    if request.method == "GET":
        modifed_themes = []
        all_themes = Theme.objects.select_related("author").all().order_by("-vote_count")
        paginator = Paginator(all_themes, 25) 
        page_number = request.GET.get('page')
        paginated_themes = paginator.get_page(page_number)
        counter = 0
        for theme in paginated_themes:
            counter += 1
            amsweres_amount = Question.objects.prefetch_related("theme").filter(theme=theme)\
                .aggregate(Sum('answer_counter'))["answer_counter__sum"]
            if amsweres_amount == None: amsweres_amount=0
            modifed_themes.append(Theme_rating(theme_slug = theme.slug,
                                            position = counter,
                                            title = theme.title,
                                            vote_count = theme.vote_count,
                                            questions_count = theme.questions_count,
                                            answer_count = amsweres_amount))
        context = {
            "modifed_themes":modifed_themes,
            "page_obj":paginated_themes,
        }
        return render(request, 'spapp/rating/rating_theme.html', context)    
    
    
    
def rating_question(request):
    if request.method == "GET":
        modifed_questions = []
        all_questions = Question.objects.all().order_by("-vote_count")
        paginator = Paginator(all_questions, 25) 
        page_number = request.GET.get('page')
        paginated_questions = paginator.get_page(page_number)
        counter = 0
        for question in paginated_questions:
            counter += 1
            modifed_questions.append(Question_rating(position = counter,
                                            slug = question.slug,
                                            title = question.title,
                                            vote_count = question.vote_count,
                                            answer_counter = question.answer_counter))
        context = {
            "modifed_questions":modifed_questions,
            "page_obj":paginated_questions,
        }
        return render(request, 'spapp/rating/rating_question.html', context)   
    
    
    
def rating_answer(request):
    if request.method == "GET":
        modifed_answers = []
        all_answers = Audio_answer.objects.select_related("question").filter(share_answer=True).order_by("-vote_count")
        paginator = Paginator(all_answers, 25) 
        page_number = request.GET.get('page')
        paginated_answers = paginator.get_page(page_number)
        counter = 0
        for answer in paginated_answers:
            counter += 1
            answer_subtitles = answer.subtitles
            if answer_subtitles:
                if len(answer_subtitles) > 40: answer_subtitles=answer_subtitles[0:38]+".."
            audio_lenght = answer.audio_lenght
            if audio_lenght: audio_lenght = (round(audio_lenght, 2))
            else: audio_lenght = 0
            words_total = answer.words_total
            if words_total: words_total = int(words_total)
            else: words_total = 0
            modifed_answers.append(Answer_rating(position = counter,
                                            subtitles = answer_subtitles,
                                            vote_count = answer.vote_count,
                                            audio_lenght = audio_lenght,
                                            words_total = words_total,
                                            answer_pk = answer.pk,
                                            qustion_slug = answer.question.slug,))
            
        context = {
            "modifed_answers":modifed_answers,
            "page_obj":paginated_answers,
        }
        return render(request, 'spapp/rating/rating_answer.html', context)   