from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from .utils import image_resizer
import datetime
from django.utils.translation import gettext_lazy as _


class Time_Stamped_Mixin(models.Model):
    """
    Abstract class for two datetime fields
    """
    created = models.DateTimeField(_('created'),auto_now_add=True)
    modified = models.DateTimeField(_('modified'),auto_now=True)
    class Meta:
        abstract = True


class User(AbstractUser):
    """
    User model
    """
    reputation = models.IntegerField(default=0)
    def __str__(self):
        return (f"User-pk:  {self.pk}")
    
    def save(self, *args, **kwargs):
        if self.reputation < 0 : self.reputation = 0
        super().save(*args, **kwargs)
    
    
def theme_directory_path(instance, filename):
    image_extension = (str(filename).split("."))[-1]
    d = datetime.datetime.now()
    year = str(f"{d.year:02d}")[2:]
    date = year + f"-{d.month:02d}-{d.day:02d}-{d.hour:02d}-{d.minute:02d}-{d.second:02d}"
    return f'theme_image/{str(slugify(instance.title)[0:50])}-{instance.author.pk}-{date}.{image_extension}'


class Theme(models.Model):
    """
    Theme which consists of questions
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 150)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to=theme_directory_path)
    time_created = models.DateTimeField(auto_now_add=True)
    vote_count = models.IntegerField(default=0)
    questions_count = models.IntegerField(default=0)
    
    def __str__(self):
        return (f"{self.title}")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.slug is None:
            new_slug =  str(slugify(self.title)[0:50])
            self.slug = new_slug
            #if used not english language
            if self.slug == "":
                self.slug = f"theme-{self.pk}"
        super().save(*args, **kwargs)
        image_resizer(self)

    
class Question(models.Model):
    """
    Question for theme
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    title = models.CharField(max_length = 160)
    time_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    answer_counter = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    
    def __str__(self):
        return (f"{self.title}")
    
    def save(self, *args, **kwargs):
        #recount all theme questions amount
        super().save(*args, **kwargs)
        self.theme.questions_count = Question.objects.filter(theme=self.theme).count()
        self.theme.save()
        #creating slug if it doesn't exist
        if self.slug is None:
            new_slug =  str(slugify(self.title)[0:50])
            self.slug = new_slug
            #if used not english language
            if self.slug == "":
                self.slug = f"question-{self.pk}"
            #if slug already exist
            if len(Question.objects.filter(slug=new_slug)) > 0:
                self.slug = f"question-{self.pk}"
            super().save(*args, **kwargs)
            
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.theme.questions_count = Question.objects.filter(theme=self.theme).count()
        self.theme.save()
    
    
class Audio_answer(models.Model):
    """
    Audio answer for question (.mp3 file)
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    subtitles = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    audio_lenght = models.FloatField(blank=True, null=True)
    words_total = models.FloatField(blank=True, null=True)
    words_per_second = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(default=0)
    share_answer = models.BooleanField(default=True)
    
    def __str__(self):
        return (f"{self.pk} >> {self.subtitles}")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        question = self.question
        all_answers = len(Audio_answer.objects.filter(question=question))
        question.answer_counter = all_answers
        question.save()
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        question = self.question
        all_answers = len(Audio_answer.objects.filter(question=question))
        question.answer_counter = all_answers
        question.save()
        

class Answer_vote(models.Model):
    """ 
    Voting for answeres 
    """
    audio_answer_id = models.ForeignKey(Audio_answer, on_delete=models.CASCADE, related_name='answer_id_vote')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id_vote')
    vote_type = models.CharField(choices=[('upvote', 'upvote'), ('downvote', 'downvote'), ], max_length=15)
    time_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Vote Answer"
    def __str__(self):
        return f"pk: {self.pk}, audio_answer_id: {self.audio_answer_id}, vote by {self.user_id}, status {self.vote_type}"


class Question_vote(models.Model):
    """ 
    Voting for questions.
    """
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_id_vote')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_user_vote')
    vote_type = models.CharField(choices=[('upvote', 'upvote'), ('downvote', 'downvote'), ], max_length=15)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vote Question"
    def __str__(self):
        return f"pk: {self.pk}, vote by {self.user_id}, status {self.vote_type}"


class Theme_vote(models.Model):
    """ 
    Voting for themes.
    """
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='theme_id_vote')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theme_user_vote')
    vote_type = models.CharField(choices=[('upvote', 'upvote'), ('downvote', 'downvote'), ], max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Vote Theme"
    def __str__(self):
        return f"pk: {self.pk}, vote by {self.user_id}, status {self.vote_type}"



class Report(Time_Stamped_Mixin):
    """
    Reports for themes/answers/questions.
    """
    class Report_status(models.TextChoices):
        APPROVED = 'approved', _('approved')
        DENIED = 'denied', _('denied')
        PENDING = 'pending', _('pending')
        
    report_sender = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="report_sender", blank=True, null=True)
    report_reciever = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="report_reciever", blank=True, null=True)
    reason = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, blank=True, null=True) 
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)
    answer = models.ForeignKey(Audio_answer, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(_('status'), max_length=15, default="pending", choices=Report_status.choices)
    
    def __str__(self):
        return (f"{self.report_sender.username} >> {self.report_reciever.username}")
    

class Reputation(Time_Stamped_Mixin):
    """
    Reputation accruals.
    """
    class Reputation_Type(models.TextChoices):
        ANSWER = 'answer', _('answer')
        QUESTION = 'question', _('question')
        THEME = 'theme', _('theme')
        
    class Vote_Type(models.TextChoices):
        UPVOTE = 'upvote', _('upvote')
        DOWNVOTE = 'downvote', _('downvote')

    amount = models.IntegerField(default=0)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reputation_reciever")
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reputation_sender")
    answer = models.ForeignKey(Audio_answer, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, blank=True, null=True) 
    type = models.CharField(_('type'), max_length=15, choices=Reputation_Type.choices)
    vote_type = models.CharField(_('vote_type'), max_length=15, choices=Vote_Type.choices)
    

class Config(models.Model):
    """
    Table with reputation score.
    """
    rep_theme_plus = models.IntegerField(default=0)
    rep_theme_minus = models.IntegerField(default=0)
    rep_question_plus = models.IntegerField(default=0)
    rep_question_minus = models.IntegerField(default=0)
    rep_answer_plus = models.IntegerField(default=0)
    rep_answer_minus = models.IntegerField(default=0)
    
    def __str__(self):
        return "Projects config"