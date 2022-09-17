from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Reputation, Theme, Question, Config
from .models import Question_vote, Theme_vote, Report
from .utils import str_to_int, get_user
from django.http import JsonResponse
import json
from .forms import New_theme_form, New_question_form 
from .forms import Edit_question_form, Edit_theme_form
from .forms import Flag_theme_form, Flag_question_form


def theme_detailed(request, theme_slug):
    if request.method == "GET":
        edited_question = request.GET.get("edited_q")
        edit_theme = request.GET.get("edit_theme")
        flagged_question = request.GET.get("flag_q")
        new_question = request.GET.get("new_q")
        deleted_question = request.GET.get("deleted_q")
        flagged_theme = request.GET.get("flag_theme")
        
        # convert string to integer for filtering
        if str_to_int(flagged_theme): flagged_theme = int(flagged_theme)
        if str_to_int(edited_question): edited_question = int(edited_question)
        if str_to_int(flagged_question): flagged_question = int(flagged_question)
        if str_to_int(new_question): new_question = int(new_question)
        
        theme_obj = get_object_or_404(Theme, slug=theme_slug)
        all_questions = Question.objects.filter(theme=theme_obj).order_by('-vote_count')
        full_share_path = request.META['wsgi.url_scheme'] + "://"+\
            request.META['HTTP_HOST'] + request.META['PATH_INFO']
        
        #get likes of your user
        user = get_user(request)
        if user:
            questions_pk_list = list(all_questions.values_list('id', flat=True))
            users_upvote_list = list(Question_vote.objects.filter(question_id__pk__in =\
                questions_pk_list, user_id = user,vote_type ='upvote').\
                    values_list('question_id', flat=True))
            users_downvote_list = list(Question_vote.objects.filter(question_id__pk__in =\
                questions_pk_list, user_id = user,vote_type ='downvote').\
                    values_list('question_id', flat=True))
            theme_vote = Theme_vote.objects.filter(theme_id=theme_obj).first()
            if theme_vote:
                if theme_vote.vote_type == "upvote": theme_vote = "upvote"
                elif theme_vote.vote_type == "downvote": theme_vote = "downvote"
            
        else:
            users_upvote_list = []
            users_downvote_list = []
            theme_vote = None

        how_many_answers = 0
        for question in all_questions:
            how_many_answers += question.answer_counter
            
        context = {"theme_obj":theme_obj,
            "all_questions":all_questions,
            "full_share_path":full_share_path,
            "new_question_form":New_question_form(),
            "flag_question_form":Flag_question_form(),
            "flag_theme_form":Flag_theme_form(),
            "edit_theme_form":Edit_theme_form(initial={'title':theme_obj.title}),
            "edit_question_form":Edit_question_form(),
            "edited_question":edited_question,
            "flagged_question":flagged_question,
            "new_question":new_question,
            "deleted_question":deleted_question,
            "flagged_theme":flagged_theme,
            "edit_theme":edit_theme,
            "users_downvote_list":users_downvote_list,
            "users_upvote_list":users_upvote_list,
            "how_many_answers":how_many_answers,
            "theme_vote":theme_vote}
        return render(request, 'spapp/theme_detailed.html', context)    
    
    elif request.method == "POST":
        edit_question_pk = request.POST.get('edit_question_pk')
        edit_theme_pk = request.POST.get("edit_theme_pk")
        flag_question_pk = request.POST.get('flag_question_pk')
        flag_theme_pk = request.POST.get('flag_theme_pk')
        new_question = request.POST.get('new_question')
        delete_theme_pk = request.POST.get("delete_theme_pk")
        delete_question_pk = request.POST.get('delete_question_pk')
        reason = request.POST.get('reason')
        
        # edit question
        if edit_question_pk:
            question = Question.objects.get(pk = edit_question_pk)
            if question.author != request.user:
                return HttpResponseRedirect(reverse("theme_detailed",args=[theme_slug]))
            theme_obj = Theme.objects.get(slug=theme_slug)
            question.title = request.POST['title']
            question.save()
            redirect = (reverse("theme_detailed",args=[theme_slug])) + \
                f"?edited_q={question.pk}" + f"#share-dialog-blok-{question.pk}"
            return HttpResponseRedirect(redirect)

        # flag question
        elif flag_question_pk:
            if reason:
                question = Question.objects.get(pk = flag_question_pk)
                user = request.user
                new_report = Report(report_sender = user, report_reciever = question.author,
                                    reason=reason,question=question)
                new_report.save()
                redirect = (reverse("theme_detailed",args=[theme_slug])) + \
                    f"?flag_q={question.pk}" + f"#share-dialog-blok-{question.pk}"
                return HttpResponseRedirect(redirect)
        
        # new question
        elif new_question:
            theme = get_object_or_404(Theme, pk=new_question)
            user = request.user
            title = request.POST.get('title')
            if not title: return HttpResponseRedirect(reverse("index"))
            new_question = Question(author = user, theme = theme,title=title)
            new_question.save()
            redirect = (reverse("theme_detailed",args=[theme_slug])) + \
                f"?new_q={new_question.pk}" + f"#share-dialog-blok-{new_question.pk}"
            return HttpResponseRedirect(redirect)
        
        # delete question
        elif delete_question_pk:
            question = Question.objects.get(pk=delete_question_pk)
            redirect = (reverse("theme_detailed",args=[theme_slug])) + \
                f"?deleted_q={question.pk}"
            question.delete()
            return HttpResponseRedirect(redirect)
        
        # flag Theme
        elif flag_theme_pk:
            theme_obj = get_object_or_404(Theme, pk=flag_theme_pk)
            user = get_user(request)
            if user and reason:
                new_report = Report(report_sender=user, report_reciever=theme_obj.author,
                                    reason=reason,theme=theme_obj).save()
                redirect = (reverse("theme_detailed",args=[theme_slug])) + \
                    f"?flag_theme={theme_obj.pk}" 
                return HttpResponseRedirect(redirect)
        
        # delete Theme
        elif delete_theme_pk:
            theme_obj = get_object_or_404(Theme, pk=delete_theme_pk)
            user = get_user(request)
            if user:
                redirect = (reverse("index")) + f"?delete_theme_title={theme_obj.title}"
                theme_obj.delete()
                return HttpResponseRedirect(redirect)
            
        # edit Theme
        elif edit_theme_pk:
            theme_obj = get_object_or_404(Theme, pk=edit_theme_pk)
            user = get_user(request)
            if user:
                theme_form = New_theme_form(request.POST, request.FILES)
                if theme_form.is_valid():
                    title = theme_form.cleaned_data['title']
                    target_image = theme_form.cleaned_data['image']
                    theme_obj.title = title
                    theme_obj.image = target_image
                    theme_obj.save()
                    redirect = (reverse("theme_detailed",args=[theme_slug])) + \
                        f"?edit_theme={theme_obj.title}" 
                    return HttpResponseRedirect(redirect)
        else:
            return HttpResponseRedirect(reverse("index"))
        
        
       
@csrf_exempt
def upvote_theme(request): 
    """ Upvote question with ajax """   
    if request.method == "POST":
        # if user is not authenticated
        user = get_user(request)
        if user == False:
            return JsonResponse({"response_status":"Not authenticated"})
        #convert <class 'bytes'> to normal dictionary
        data = json.loads(request.body.decode("utf-8").replace("'",'"'))

        current_counter = int(data["current_counter"])
        theme_id = int(data["theme_id"])
        theme_obj = Theme.objects.get(pk = theme_id)

        if theme_obj.author == user:
            return JsonResponse({"response_status":"can't upvote your own question"})
        vote_type = str(data["vote_type"])
        status = "error"
        # downvote_recieved, 3 scenarios,  current_counter == 1 | == -1 | == - 2
        if vote_type == "upvote":
            if current_counter == 2:
                #vote exist (it was disliked, now it is liked)
                theme_vote_object_defaults = {'vote_type':vote_type}
                theme_vote_object, created = Theme_vote.objects.update_or_create(
                    theme_id=theme_obj,user_id=user, defaults=theme_vote_object_defaults)
                status = "upvote_from_downvote" 
            elif current_counter == 1:
                #vote doesn't exist yet
                theme_vote_object_defaults = {'vote_type':vote_type}
                theme_vote_object, created = Theme_vote.objects.update_or_create(
                    theme_id=theme_obj,user_id=user, defaults=theme_vote_object_defaults)
                status = "upvote_first_time"
            elif current_counter == -1:
                #vote exist, it was already liked, now it is neither liked, nor disliked
                try:
                    theme_vote_object = Theme_vote.objects.get(
                        theme_id=theme_obj,user_id=user)
                    theme_vote_object.delete()
                    status = "upvote_cancel"
                except:
                    response_status = {"response_status":'error vote answer not found'}
                    return JsonResponse(response_status)
            #update votes for an theme         
            all_theme_upvotes = len(Theme_vote.objects.filter(theme_id = theme_obj, vote_type = "upvote"))
            all_theme_downvotes = len(Theme_vote.objects.filter(theme_id = theme_obj, vote_type = "downvote"))
            current_vote_for_answer = all_theme_upvotes - all_theme_downvotes
            theme_obj.vote_count = current_vote_for_answer
            theme_obj.save()
            
        #accrual of reputation
        sender = user
        reciver = theme_obj.author
        upvote_rep_amount = Config.objects.all().first().rep_theme_plus
        downvote_rep_amount = Config.objects.all().first().rep_theme_minus
        reputation_query = Reputation.objects.filter(reciever=reciver, sender=sender, theme=theme_obj)
        reputation_obj = reputation_query.first()
        # if reputation exists, and it is CANCELING from upvote
        if len(reputation_query) > 0 and reputation_obj.vote_type == 'upvote':
            reputation_obj.delete()
            reciver.reputation -= upvote_rep_amount
            reciver.save()
            
        # if reputation exists, and it is UPVOTE from downvote
        elif len(reputation_query) > 0 and reputation_obj.vote_type == 'downvote':
            reciver.reputation += upvote_rep_amount + (downvote_rep_amount * -1)
            reciver.save()
            reputation_obj.vote_type = 'upvote'
            reputation_obj.amount = upvote_rep_amount
            reputation_obj.save()
        
        # if reputation obj doesn't exist, create reputation object
        elif len(reputation_query) == 0:
            reputation_obj = Reputation(amount = upvote_rep_amount,reciever=reciver,
                                        sender=sender, theme=theme_obj,type='theme',
                                        vote_type='upvote').save()
            reciver.reputation += upvote_rep_amount
            reciver.save()
        
        response_status = {"response_status":status}
        return JsonResponse(response_status)
    
    
@csrf_exempt
def downvote_theme(request):    
    if request.method == "POST":
        # if user is not authenticated
        user = get_user(request)
        if user == False:
            return JsonResponse({"response_status":"Not authenticated"})

        #convert <class 'bytes'> to normal dictionary
        data = json.loads(request.body.decode("utf-8").replace("'",'"'))
        current_counter = int(data["current_counter"])
        theme_id = int(data["theme_id"])
        theme_obj = Theme.objects.get(pk = theme_id)
        if theme_obj.author == user:
            return JsonResponse({"response_status":"can't downvote your own question"})
        vote_type = str(data["vote_type"])
        status = "error"
        # downvote_recieved, 3 scenarios,  current_counter == 1 | == -1 | == - 2
        if vote_type == "downvote": 
            if current_counter == -2:
                #vote exist (it was liked, now it is disliked)
                theme_vote_object_defaults = {'vote_type':vote_type}
                theme_vote_object, created = Theme_vote.objects.update_or_create(
                    theme_id=theme_obj,user_id=user, defaults=theme_vote_object_defaults)
                status = "downvote_from_upvote" 
            elif current_counter == -1:
                #vote doesn't exist yet
                theme_vote_object_defaults = {'vote_type':vote_type}
                theme_vote_object, created = Theme_vote.objects.update_or_create(
                    theme_id=theme_obj,user_id=user, defaults=theme_vote_object_defaults)
                status = "downvote_first_time"
            elif current_counter == 1:
                #vote exist, it was already disliked, now it is neither disliked, nor liked
                try:
                    theme_vote_object = Theme_vote.objects.get(
                        theme_id=theme_obj,user_id=user)
                    theme_vote_object.delete()

                    status = "downvote_cancel"
                except:
                    response_status = {"response_status":'error vote answer not found'}
                    return JsonResponse(response_status)          
            #update votes for an theme         
            all_theme_upvotes = len(Theme_vote.objects.filter(theme_id = theme_obj, vote_type = "upvote"))
            all_theme_downvotes = len(Theme_vote.objects.filter(theme_id = theme_obj, vote_type = "downvote"))
            current_vote_for_answer = all_theme_upvotes - all_theme_downvotes
            theme_obj.vote_count = current_vote_for_answer
            theme_obj.save()

        # decrease reputation
        sender = user
        reciver = theme_obj.author
        upvote_rep_amount = Config.objects.all().first().rep_theme_plus
        downvote_rep_amount = Config.objects.all().first().rep_theme_minus
        reputation_query = Reputation.objects.filter(reciever=reciver, sender=sender, theme=theme_obj)
        reputation_obj = reputation_query.first()
        # if reputation exists, and it is canceling
        if len(reputation_query) > 0 and reputation_obj.vote_type == 'downvote':
            reputation_query.first().delete()
            reciver.reputation -= downvote_rep_amount
            reciver.save()
        
        # if reputation exists, and it is DOWNVOTE from upvote
        elif len(reputation_query) > 0 and reputation_obj.vote_type == 'upvote':
            reciver.reputation -=  (upvote_rep_amount - downvote_rep_amount)
            reciver.save()
            reputation_obj.vote_type = 'downvote'
            reputation_obj.amount = downvote_rep_amount
            reputation_obj.save()
        
        # if reputation obj doesn't exist
        elif len(reputation_query) == 0:
            reputation_obj = Reputation(amount = downvote_rep_amount,reciever=reciver,
                                        sender=sender, theme=theme_obj,type='theme',
                                        vote_type='downvote').save()
            reciver.reputation += downvote_rep_amount
            reciver.save()
            
        response_status = {"response_status":status}
        return JsonResponse(response_status)

