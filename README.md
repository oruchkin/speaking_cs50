# Capstone - Speaking club

## Idea:

The purpose in the life of this project is to let user speak english out loud.

## What problem this project solve:

Speaking club allows the user to practice their speaking skills, and practice listening skills as a by-product.

## Distinctiveness and Complexity:

**Why it is unique:**

The only similarity with older projects that this project has "upvotes and downvotes", and you might compare it with "network" project, but i'm sure if i delete this "upvotes and downvotes" from the "speaking club" project, it still will be a complete project, because voting system is only an addition to the project, but not its basis. Project would exist without voting.
I also wanted to add followings in this project, but decided against it, because it would look like network, but it isn't.
I took inspiration from the stackoverflow project, and you can find similarities in it.

**Complexity:**

This project has:

- 11 models, one of which is abstract
- 7 java scripts, each of which has many functions inside
- 7 different views scipts
- Script for forms ( forms.py )
- Script for dataclasses ( dataclasses.py )
- Script for utils ( utils.py )
- Script for helper functions ( helpers.py )
- Custom filters for .html pages ( /templatetags/spapp/filters.py )
- Custom admin panel ( admin.py )

# How to run your application (this appliction)

this application has requirements.txt with all of the libraries that you need.

But this is not all, you also need to install "ffmpeg". This is not a library, this program installs globally on your computer, and can't be installed in virtuall environment.
Ffmpeg is very popular software to convert videos and audios, i use it in speaking club to convert audio after it is recorder and sended to server by user.  (i will type about this algorithm how it works later in appropriate part)

If you don't want to install "ffmpeg" globally, i believe you still would be abble to start this project on your local computer, but some libraries might not be installed, because they require "ffmpeg". And part where user creating answer won't work without ffmpeg.
Also i uploaded this project on my virtual machine, and you can check it online https://speakingclub.com

I believe i don't need to give instructions how to install ffmpeg, because it depends on Operation System you have. You need to go through it by yourself :'(

Complete algorithm how to start "speaking club" on your computer:

1) install ffmpeg
2) install all the requirements from requirements.txt with command "pip3 install -r requiremets.txt" (i recommend to install it in virtual environment)
3) start project with command "python3 manage.py runserver 0.0.0.0:8000"
4) go to you localhost in browser "http://127.0.0.1:8000"
5) Success! It is online! (it has to be)

# What’s contained in each file you created:

In this section i will describe step by step all the content which was shorty described in "Complexity" section (and some more):

**settings.py:**

- project starts with it's "**settings.py**" it devided by components in "components" folder it is done with **django-split-settings==1.1.0** library (looks better for me)

**urls.py:**

- in app's "**urls.py**" you can see all paths that this project uses, it is also splitted by comments in parts

**Views:**

- as you could see in urls.py project has different "views", this is done to split scripts so they wouldn't be very big, we have:
- *views_answer.py* - it is responsible for the logic with answers (upvote/downvote/share/save audio from frontend/generate subtitles)
- *views_auth.py  -* it is responsible for the logic with registration and authorisation and displaying its pages
- *views_profile.py  -* it is responsible for displaying all users profile pages
- *views_question.py -* it is responsible for displaying all users profile pages (upvote/downvote/create/delete/display)
- *views_rating.py -* it is responsible for displaying all ratings data pages
- *views_question.py -* it is responsible for logic with themes (upvote/downvote/create/delete/display)
- *views_rating.py -* it is responsible for displaying all ratings data pages

**Forms.py**

- forms.py consist of forms which are used on .html pages to create/edit themes, questions, and answers

**Models.py**

 There are 11 models:

- Time_Stamped_Mixin - abstract model which inherit by itself "created" and "modified" fields to other models
- User - model of the user
- Theme - model of theme, it has "theme_directory_path" in image upload section which direct theme to its folder and rename it, also it hase rewriten "save" method which call "image_resizer" function, which process image after it is being uploaded by user, and does two function, resize  and compress image
- Question - question model, it also has rewriten save and delete method, save method recount how many questions have theme after question saved, delete method does the same but after question was deleted
- Audio_answer - this is model where .mp3 filed being stored, (most important model), it has rewriten save and delete methods, they recount answers after "audio_answer" model being saved or deleted, and write it in question's answer_counter field
- Answer_vote - model responsible for voting for answers
- Question_vote - model responsible for voting for questions
- Theme_vote - model responsible for voting for themes
- Report - model for reports, it take all three possible report types in itself, theme/question/answer
- Reputation - model responsible for responsible for counting votes
- Config - model which have data of how much reputation one upvote and downvote for each theme/question/answer cost. Project can have only one config, you can't create or delete config in admin panel (it is restricted in admin.py)

**Dataclasses.py**

- This is actually very intresting part, what do dataclasses do?

Dataclasses are used in **views_rating.py**, their purpose in life to create a list of objects, which is later used in **rating pages**

- Why did i use them?

i could do ratings without dataclasses, BUT, it would be with more querys to database.
As you can see all functions: "*rating_answer, rating_question, rating_theme, rating_user"* are only using ONE query to database for such a complex task as providing ratings. With dataclasses i was able to gather all data i need to ratings in backend without using any frontend logic, such as filters for examples. And on the ratings.html pages, i used dataclasses, not query set to show data, but i also used in parallel queryset for pagination, it works together perfectly. My query set by defualt has not enoung data for example it has no link for user's avatar, no position in rating etc., and thus i needed something more than just queryset.
So i have only ONE query to database, and all logic on backend in ONE place, thanks to dataclasses.

**Utils.py**

in utils i have functions to recize images for themes, and also i have helper functions such as *"str_to_int, get_user, member_for"*

**Helpers.py**

I think, this script should be together with utils.py in one script. But it is okay, it is responsible for geting subtitles, it has two functions, but only one of them "get_large_audio_transcription2" is actually working, i decided to keep both of them on the future. This function split audio file in chunks and send it to google api via speech recognition library, and returns subtitles of the answer back to us.

**Filters.py**

i have 3 filters here (they are in templatetags folder), one of them is prety cool (others are bad):

- "gravatar_url" this filter returns an avatar depending on the user's email. So each avatar is UNIQUE, and i don't need to save this avatar's on my hdd, i took this idea from stackoverflow, they use same technique.
- profile_reputation_title and profile_reputation_link: this filters are responsible for displaying reputation box in users profile. Why do i need it? As you remember from models.py "Reputation" model has 3 different foreing keys inside of itself "theme/question/answer" but i need to show user where his reputation come from, so this filters do this for me.

This two last filters are actually very bad, i regret using them, but they do their job, you may ask: "Why are this filters bad?"
And i answer: "This is a very good question! Thank you for asking!"

When ever this filters triggered they create a query for a database, and you can imagine user have 10-50-1000 database entries, and for each of which this filter would create a query to database, so it would spam database with its querys.

What can i do with it? I can create a dataclass, and instead of creating new queries to database with filters each time, i could do it with dataclasses on my backend, and send it to frontend with only ONE query to database and all logic on my server. Problem only will occur if there would be a lot of users, for now its okay.

**Admin.py - admin panel**

in admin panel you may find intresting:

- fields "autocomplete_fields" autocomplete_fields which preload the database, and you can do convenient search by foreing key
- Config - i restricted deletiong and adding new config files, because you only need one config for this project
- Theme_Admin - it has a cool preview of image inside of each object
- Report_Admin - this model is most intresting, from here you can hit a link "reason link" and it will move you to the place where report was triggered. It also has custom filters "Report_type_Filter"

**7 java scripts, each of which has many functions inside** 

javascripts are in /static/js folder

- audioplayer.js - responsible for displaying a beautiful skin for the audio player
- sound_recorder.js - has several functions in itself, it is responsible for:

  1. rendering  in "make audio answer page" buttons, audio player,
  2. recording audio
  3. triggering generation of subtitles
  4. sending this audion via ajax (with jquery) to backend, which would process it and save it as an asnwer
  5. redirecting user in the end
- theme_detailed.js - responsible for theme and question logic (share theme/question, and vocalizing question with robot voice)
- toast.js - shows to user toast, it triggerd when user upvote/downvote him self, or if user is not authorised and still want to upvote/downvote someone
- vote_answer.js - responsible for upvote/downvote answers, and also for toggling "share answer publicly" button
- vote_question.js - responsible for upvote/downvote questions
- vote_theme.js - responsible for upvote/downvote themes

---

This project is online:
https://speakingclub.space

in default sqlite database you can login as admin:

login: **admin**

pass: **admin**

---
Feel free to contact me if you have any questions

telegram: **@oruchkin**

email: **oruchkin@bk.ru**
