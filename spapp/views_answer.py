from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
from pydub import AudioSegment
import ffmpeg
import json
from .models import Reputation, Question, Audio_answer
from .models import Answer_vote, Config
from .helpers import get_large_audio_transcription
from .utils import get_user
import datetime


import os
import shutil

@csrf_exempt
def subtitle_generator(request):    
    if request.method == "POST":
        user = request.user
        audio_file = request.FILES['file']
        question_pk = request.POST["question_pk"]
        question = Question.objects.get(pk=question_pk)
        new_answer = Audio_answer.objects.create(author=user, question = question, audio_file= audio_file)
        new_answer.save()
        
        #ffmpeg converting file to normal state
        sound =  AudioSegment.from_file(new_answer.audio_file.path)
        sound.export(new_answer.audio_file.path, format="wav")
        
        #renaming file and resaving it
        new_name = 'audio/' + str(f'answer-{new_answer.pk}.wav')
        os.rename(new_answer.audio_file.path, settings.MEDIA_ROOT + new_name)
        new_answer.audio_file.name = new_name
        try:
            new_answer.subtitles = str(get_large_audio_transcription(new_answer.audio_file.path))
        except:
            result = {"status":"fail", 'message':'cant process'}
            new_answer.delete()
            return JsonResponse(result)
        audio_lenght = float(ffmpeg.probe(new_answer.audio_file.path)['format']['duration'])
        
        sentence = new_answer.subtitles 
        words_counter = 1;  
        for i in range(0, len(sentence)-1):  
            #Counts all the spaces present in the string  
            #It doesn't include the first space as it won't be considered as a word  
            if(sentence[i] == ' ' and sentence[i+1].isalpha() and (i > 0)):  
                words_counter = words_counter + 1;  
                
        words_per_second = round(words_counter/audio_lenght, 2)
        new_answer.words_per_second = words_per_second
        new_answer.words_total = words_per_second
        new_answer.audio_lenght = audio_lenght
        new_answer.save()

        result = {"status":"success", 
                  'subtitles':new_answer.subtitles, 
                  'audio_lenght':audio_lenght, 
                  'words_counter':words_counter,
                  'words_per_second':words_per_second}
        new_answer.delete()
        return JsonResponse(result)
    
    
@csrf_exempt
def save_audio_answer(request):    
    if request.method == "POST":
        try:
            user = request.user
            share_answer = request.POST['check_box_share']
            if share_answer == "false": share_answer = False
            if share_answer == "true": share_answer = True
            audio_file = request.FILES['file']
            question_pk = request.POST["question_pk"]
            edited_subtitles = request.POST["edited_subtitles"]
            words_counter_int = request.POST["words_counter_int"]
            audio_lenght_int = request.POST["audio_lenght_int"]
            words_per_second_int = request.POST["words_per_second_int"]
            if (edited_subtitles == "undefined") or (words_counter_int == "undefined") or (audio_lenght_int == "undefined"):
                result = {"status":"fail", "reason": "no data"}
                return JsonResponse(result)
            question = Question.objects.get(pk=question_pk)
            new_answer = Audio_answer.objects.create(author=user, question = question, audio_file= audio_file, 
                                                    subtitles=edited_subtitles, words_total=words_counter_int,
                                                    words_per_second=words_per_second_int,audio_lenght=audio_lenght_int,
                                                    share_answer=share_answer)
            new_answer.save()
            
            #ffmpeg converting file to normal state
            sound =  AudioSegment.from_file(new_answer.audio_file.path)
            sound.export(new_answer.audio_file.path, format="mp3")
            
            #renaming file and resaving it with creating folders
            date_path = f"{datetime.date.today().year}/{datetime.date.today().month}/{datetime.date.today().day}/"
            dir = settings.MEDIA_ROOT+ 'audio/' + date_path
            try:
                os.makedirs(dir)
            except OSError:
                pass
            new_name = 'audio/' + date_path + str(f'answer-{new_answer.pk}.mp3')
            os.replace(new_answer.audio_file.path, settings.MEDIA_ROOT + new_name)
            new_answer.audio_file.name = new_name
            new_answer.save()
            result = {"status":"success", 'saved':"yes", 'question_slug':question.slug, 'answer_pk':new_answer.pk}
            return JsonResponse(result)
        except:
            result = {"status":"fail"}
            return JsonResponse(result)
    
    
@csrf_exempt
def downvote_answer(request):    
    if request.method == "POST":
        # if user is not authenticated
        user = get_user(request)
        if user == False:
            return JsonResponse({"response_status":"Not authenticated"})

        #convert <class 'bytes'> to normal dictionary
        data = json.loads(request.body.decode("utf-8").replace("'",'"'))
        current_counter = int(data["current_counter"])
        answer_id = int(data["answer_id"])
        answer_obj = Audio_answer.objects.get(pk = answer_id)
        if answer_obj.author == user:
            return JsonResponse({"response_status":"can't downvote your own answer"})
        vote_type = str(data["vote_type"])
        status = "error"
        # downvote_recieved, 3 scenarios,  current_counter == 1 | == -1 | == - 2
        if vote_type == "downvote": 
            if current_counter == -2:
                #vote exist (it was liked, now it is disliked)
                answer_vote_object_defaults = {'vote_type':vote_type}
                answer_vote_object, created = Answer_vote.objects.update_or_create(
                    audio_answer_id=answer_obj,user_id=user, defaults=answer_vote_object_defaults)
                status = "downvote_from_upvote" 
            elif current_counter == -1:
                #vote doesn't exist yet
                answer_vote_object_defaults = {'vote_type':vote_type}
                answer_vote_object, created = Answer_vote.objects.update_or_create(
                    audio_answer_id=answer_obj,user_id=user, defaults=answer_vote_object_defaults)
                status = "downvote_first_time"
            elif current_counter == 1:
                #vote exist, it was already disliked, now it is neither disliked, nor liked
                try:
                    answer_vote_object = Answer_vote.objects.get(
                        audio_answer_id=answer_obj,user_id=user)
                    answer_vote_object.delete()

                    status = "downvote_cancel"
                except:
                    response_status = {"response_status":'error vote answer not found'}
                    return JsonResponse(response_status)
            #update votes for an answer
            all_answer_upvotes = len(Answer_vote.objects.filter(audio_answer_id = answer_obj, vote_type = "upvote"))
            all_answer_downvotes = len(Answer_vote.objects.filter(audio_answer_id = answer_obj, vote_type = "downvote"))
            current_vote_for_answer = all_answer_upvotes - all_answer_downvotes
            answer_obj.vote_count = current_vote_for_answer
            answer_obj.save()

        # decrease reputation
        sender = user
        reciver = answer_obj.author
        upvote_rep_amount = Config.objects.all().first().rep_answer_plus
        downvote_rep_amount = Config.objects.all().first().rep_answer_minus
        reputation_query = Reputation.objects.filter(reciever=reciver, sender=sender, answer=answer_obj)
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
                                        sender=sender, answer=answer_obj,type='answer',
                                        vote_type='downvote').save()
            reciver.reputation += downvote_rep_amount
            reciver.save()
            
        response_status = {"response_status":status}
        return JsonResponse(response_status)
    
    
@csrf_exempt
def upvote_answer(request):    
    if request.method == "POST":
        # if user is not authenticated
        user = get_user(request)
        if user == False:
            return JsonResponse({"response_status":"Not authenticated"})
        #convert <class 'bytes'> to normal dictionary
        data = json.loads(request.body.decode("utf-8").replace("'",'"'))

        current_counter = int(data["current_counter"])
        answer_id = int(data["answer_id"])
        answer_obj = Audio_answer.objects.get(pk = answer_id)
        if answer_obj.author == user:
            return JsonResponse({"response_status":"can't upvote your own answer"})
        vote_type = str(data["vote_type"])
        status = "error"
        # downvote_recieved, 3 scenarios,  current_counter == 1 | == -1 | == - 2
        if vote_type == "upvote":
            if current_counter == 2:
                #vote exist (it was disliked, now it is liked)
                answer_vote_object_defaults = {'vote_type':vote_type}
                answer_vote_object, created = Answer_vote.objects.update_or_create(
                    audio_answer_id=answer_obj,user_id=user, defaults=answer_vote_object_defaults)
                status = "upvote_from_downvote" 
            elif current_counter == 1:
                #vote doesn't exist yet
                answer_vote_object_defaults = {'vote_type':vote_type}
                answer_vote_object, created = Answer_vote.objects.update_or_create(
                    audio_answer_id=answer_obj,user_id=user, defaults=answer_vote_object_defaults)
                status = "upvote_first_time"
            elif current_counter == -1:
                #vote exist, it was already liked, now it is neither liked, nor disliked
                try:
                    answer_vote_object = Answer_vote.objects.get(
                        audio_answer_id=answer_obj,user_id=user)
                    answer_vote_object.delete()
                    status = "upvote_cancel"
                except:
                    response_status = {"response_status":'error vote answer not found'}
                    return JsonResponse(response_status)
            #update votes for an answer         
            all_answer_upvotes = len(Answer_vote.objects.filter(audio_answer_id = answer_obj, vote_type = "upvote"))
            all_answer_downvotes = len(Answer_vote.objects.filter(audio_answer_id = answer_obj, vote_type = "downvote"))
            current_vote_for_answer = all_answer_upvotes - all_answer_downvotes
            answer_obj.vote_count = current_vote_for_answer
            answer_obj.save()
            
        # accrual of reputation
        sender = user
        reciver = answer_obj.author
        upvote_rep_amount = Config.objects.all().first().rep_answer_plus
        downvote_rep_amount = Config.objects.all().first().rep_answer_minus
        reputation_query = Reputation.objects.filter(reciever=reciver, sender=sender, answer=answer_obj)
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
                                        sender=sender, answer=answer_obj,type='answer',
                                        vote_type='upvote').save()
            reciver.reputation += upvote_rep_amount
            reciver.save()
        
        response_status = {"response_status":status}
        return JsonResponse(response_status)
    
    
@csrf_exempt
def ajax_share_answer(request):    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8").replace("'",'"'))
            user = request.user
            toggle_share_answer_id = data["toggle_share_answer_id"]
            toggle_state = data["toggle_state"]
            audio_answer = Audio_answer.objects.get(pk=toggle_share_answer_id)
            if audio_answer.author != user:
                return JsonResponse({"no_access":"here_1"})
            audio_answer.share_answer = toggle_state
            audio_answer.save()
            response_status = {"audio_answer":toggle_state}
            return JsonResponse(response_status)
        except:
            return JsonResponse({"no_access":"here_2"})


