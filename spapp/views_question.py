from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import Reputation, Question, Audio_answer, Config
from .models import Answer_vote, Question_vote, Report
from .utils import str_to_int, get_user



def question_detailed(request, q_slug, message=None):
    if request.method == "GET":
        # get created or deleted question message
        answer_pk_deleted = request.GET.get('ans_pk')
        del_number = request.GET.get('del')
        flagged = request.GET.get('flagged')
        answer_fail = request.GET.get('answer_fail')
        
        
        if str_to_int(flagged): flagged = int(flagged)
        if str_to_int(del_number): del_number = int(del_number)
        if del_number == 1:
            message = f"Answer number '{answer_pk_deleted}' - has been deleted successfully"
        elif del_number == 2:  message = f"Answer created successfully"
        else: message = None
        
        question_obj = Question.objects.get(slug=q_slug)
        theme = question_obj.theme
        # get ammount of users answers
        user = get_user(request)
        if user:
            users_answers_ammount = len(Audio_answer.objects.filter(question = question_obj, author = user))
        else:
            users_answers_ammount = None
        
        all_answers = Audio_answer.objects.filter(question = question_obj).order_by('-vote_count')
        #sorting answers which we need to show and which not (shared, or not shared)
        all_answers_share_formated = []
        for answer in all_answers:
            if answer.author == user:
                all_answers_share_formated.append(answer.pk)
            elif answer.share_answer == True:
                all_answers_share_formated.append(answer.pk)
        all_answers = Audio_answer.objects.filter(id__in = all_answers_share_formated).order_by("-vote_count")
            
        if question_obj.answer_counter != len(all_answers):
            question_obj.answer_counter == len(all_answers)
            question_obj.save()
        full_share_path = request.META['wsgi.url_scheme'] + "://"+\
            request.META['HTTP_HOST'] + request.META['PATH_INFO']
        #get likes of your user
        answers_pk_list = list(all_answers.values_list('id', flat=True))
        users_upvote_list = list(Answer_vote.objects.filter(audio_answer_id__pk__in =\
            answers_pk_list, user_id = user,vote_type ='upvote').\
                values_list('audio_answer_id', flat=True))
        users_downvote_list = list(Answer_vote.objects.filter(audio_answer_id__pk__in =\
            answers_pk_list, user_id = user,vote_type ='downvote').\
                values_list('audio_answer_id', flat=True))
        
        return render(request, 'spapp/question_detailed.html',{
            "question_obj":question_obj,
            "all_answers":all_answers,
            "users_answers_ammount":users_answers_ammount,
            "theme":theme,
            "message":message,
            "users_downvote_list":users_downvote_list,
            "users_upvote_list":users_upvote_list,
            "full_share_path":full_share_path,
            "flagged":flagged,
            "answer_fail":answer_fail,
        })    
    
    if request.method == "POST":
        edit_answer_pk = request.POST.get('edit_answer_pk')
        answer_subtiltes = request.POST.get('answer_subtiltes')
        flag_answer_pk = request.POST.get('flag_answer_pk')
        flag_answer_reason = request.POST.get('flag_answer_reason')
        user = get_user(request)
        
        # edit answer
        if edit_answer_pk and answer_subtiltes:
            audio_answer = Audio_answer.objects.get(pk=edit_answer_pk)
            audio_answer.subtitles = answer_subtiltes
            audio_answer.save()
            return HttpResponseRedirect(reverse("question_detailed", args=[q_slug])+f"#{edit_answer_pk}")
            
        # flag answer
        elif flag_answer_pk and flag_answer_reason and user:
            audio_answer = Audio_answer.objects.get(pk=flag_answer_pk)
            new_report = Report(report_sender=user, report_reciever=audio_answer.author,
                                reason=flag_answer_reason,answer=audio_answer).save()
            redirect = reverse("question_detailed", args=[audio_answer.question.slug])+ \
                f"?flagged={audio_answer.pk}#{audio_answer.pk}"
            return HttpResponseRedirect(redirect)
        return HttpResponseRedirect(reverse("index"))
        
        
@csrf_exempt
def upvote_question(request): 
    """ Upvote question with ajax """   
    if request.method == "POST":
        # if user is not authenticated
        user = get_user(request)
        if user == False:
            return JsonResponse({"response_status":"Not authenticated"})
        #convert <class 'bytes'> to normal dictionary
        data = json.loads(request.body.decode("utf-8").replace("'",'"'))

        current_counter = int(data["current_counter"])
        question_id = int(data["question_id"])
        question_obj = Question.objects.get(pk = question_id)

        if question_obj.author == user:
            return JsonResponse({"response_status":"can't upvote your own question"})
        vote_type = str(data["vote_type"])
        status = "error"
        # downvote_recieved, 3 scenarios,  current_counter == 1 | == -1 | == - 2
        if vote_type == "upvote":
            if current_counter == 2:
                #vote exist (it was disliked, now it is liked)
                question_vote_object_defaults = {'vote_type':vote_type}
                question_vote_object, created = Question_vote.objects.update_or_create(
                    question_id=question_obj,user_id=user, defaults=question_vote_object_defaults)
                status = "upvote_from_downvote" 
            elif current_counter == 1:
                #vote doesn't exist yet
                question_vote_object_defaults = {'vote_type':vote_type}
                question_vote_object, created = Question_vote.objects.update_or_create(
                    question_id=question_obj,user_id=user, defaults=question_vote_object_defaults)
                status = "upvote_first_time"
            elif current_counter == -1:
                #vote exist, it was already liked, now it is neither liked, nor disliked
                try:
                    question_vote_object = Question_vote.objects.get(
                        question_id=question_obj,user_id=user)
                    question_vote_object.delete()
                    status = "upvote_cancel"
                except:
                    response_status = {"response_status":'error vote answer not found'}
                    return JsonResponse(response_status)
            #update votes for an answer         
            all_question_upvotes = len(Question_vote.objects.filter(question_id = question_obj, vote_type = "upvote"))
            all_question_downvotes = len(Question_vote.objects.filter(question_id = question_obj, vote_type = "downvote"))
            current_vote_for_answer = all_question_upvotes - all_question_downvotes
            question_obj.vote_count = current_vote_for_answer
            question_obj.save()
            
        # accrual of reputation
        sender = user
        reciver = question_obj.author
        upvote_rep_amount = Config.objects.all().first().rep_question_plus
        downvote_rep_amount = Config.objects.all().first().rep_question_minus
        reputation_query = Reputation.objects.filter(reciever=reciver, sender=sender, question=question_obj)
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
                                        sender=sender, question=question_obj,type='question',
                                        vote_type='upvote').save()
            reciver.reputation += upvote_rep_amount
            reciver.save()
        
        response_status = {"response_status":status}
        return JsonResponse(response_status)
    
    
@csrf_exempt
def downvote_question(request):    
    if request.method == "POST":
        # if user is not authenticated
        user = get_user(request)
        if user == False:
            return JsonResponse({"response_status":"Not authenticated"})

        #convert <class 'bytes'> to normal dictionary
        data = json.loads(request.body.decode("utf-8").replace("'",'"'))
        current_counter = int(data["current_counter"])
        question_id = int(data["question_id"])
        question_obj = Question.objects.get(pk = question_id)
        if question_obj.author == user:
            return JsonResponse({"response_status":"can't downvote your own question"})
        vote_type = str(data["vote_type"])
        status = "error"
        # downvote_recieved, 3 scenarios,  current_counter == 1 | == -1 | == - 2
        if vote_type == "downvote": 
            if current_counter == -2:
                #vote exist (it was liked, now it is disliked)
                question_vote_object_defaults = {'vote_type':vote_type}
                question_vote_object, created = Question_vote.objects.update_or_create(
                    question_id=question_obj,user_id=user, defaults=question_vote_object_defaults)
                status = "downvote_from_upvote" 
            elif current_counter == -1:
                #vote doesn't exist yet
                question_vote_object_defaults = {'vote_type':vote_type}
                question_vote_object, created = Question_vote.objects.update_or_create(
                    question_id=question_obj,user_id=user, defaults=question_vote_object_defaults)
                status = "downvote_first_time"
            elif current_counter == 1:
                #vote exist, it was already disliked, now it is neither disliked, nor liked
                try:
                    question_vote_object = Question_vote.objects.get(
                        question_id=question_obj,user_id=user)
                    question_vote_object.delete()

                    status = "downvote_cancel"
                except:
                    response_status = {"response_status":'error vote answer not found'}
                    return JsonResponse(response_status)
            #update votes for an answer            
            all_question_upvotes = len(Question_vote.objects.filter(question_id = question_obj, vote_type = "upvote"))
            all_question_downvotes = len(Question_vote.objects.filter(question_id = question_obj, vote_type = "downvote"))
            current_vote_for_answer = all_question_upvotes - all_question_downvotes
            question_obj.vote_count = current_vote_for_answer
            question_obj.save()

        # decrease reputation
        sender = user
        reciver = question_obj.author
        upvote_rep_amount = Config.objects.all().first().rep_answer_plus
        downvote_rep_amount = Config.objects.all().first().rep_answer_minus
        reputation_query = Reputation.objects.filter(reciever=reciver, sender=sender, question=question_obj)
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
                                        sender=sender, question=question_obj,type='question',
                                        vote_type='downvote').save()
            reciver.reputation += downvote_rep_amount
            reciver.save()
            
        response_status = {"response_status":status}
        return JsonResponse(response_status)