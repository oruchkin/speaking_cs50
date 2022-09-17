from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter
from . models import User, Theme, Question, Config, Reputation, Report
from . models import Answer_vote, Audio_answer, Question_vote, Theme_vote

@admin.register(User)
class User_Admin(admin.ModelAdmin):
    readonly_fields = ['password']
    filter_horizontal = ['groups', 'user_permissions']
    search_fields = ['username','email', 'pk']
    list_display = ['username','email', 'pk']


@admin.register(Theme)
class Theme_Admin(admin.ModelAdmin):
    search_fields = ['title','author__email', 'pk', 'author__username']
    list_display = ['title','author', 'time_created','vote_count']
    autocomplete_fields = ['author']
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-width: 400px;">')
    preview.short_description = 'Image'
    def get_readonly_fields(self, request, obj=None):
        return ['preview']


@admin.register(Question)
class Question_Admin(admin.ModelAdmin):
    search_fields = ['title','author__email', 'pk', 'author__username']
    list_display = ['title','theme', 'time_created','vote_count', 'answer_counter', 'get_author_email']
    autocomplete_fields = ['author', 'theme']
    search_fields = ['pk']
    def get_author_email(self,obj):
        return obj.author.email
    get_author_email.short_description = "author email"


class Report_type_Filter(SimpleListFilter):
    title = 'Report_type'
    parameter_name = 'report_type'
    def lookups(self, request, model_admin):
        return (('question', "Question"),
                ("answer", "Answer"),
                ("theme", "Theme"))
    def queryset(self, request, queryset):
        if self.value() == 'question':
            return queryset.filter(question__isnull=False)
        elif self.value() == 'answer':
            return queryset.filter(answer__isnull=False)
        elif self.value() == 'theme':
            return queryset.filter(theme__isnull=False)


@admin.register(Report)
class Report_Admin(admin.ModelAdmin):
    search_fields = ['report_sender__email','report_reciever__email', 'report_sender__username', 'report_reciever__username']
    list_display = ['report_sender', 'is_active','status','report_type', 'reason_link','reason','created','modified']
    list_filter = ['is_active',Report_type_Filter, 'status']
    autocomplete_fields = ['report_sender','report_reciever']
    readonly_fields = ['created', 'modified']
    autocomplete_fields = ['report_sender', 'report_reciever','theme','question','answer']
    def report_type(self,obj):
        if obj.question: return "Question"
        elif obj.theme: return "Theme"
        elif obj.answer: return "Answer"
        else: return None
    def reason_link(self, obj):
        link='link to reason'
        if obj.question:
            return format_html(f"<a href='/theme_detailed/{obj.question.theme.slug}#share-dialog-blok-{obj.question.pk}'>{link}</a>")
        elif obj.theme:
            return format_html(f"<a href='/theme_detailed/{obj.theme.slug}'>{link}</a>")
        elif obj.answer:
            return format_html(f"<a href='/question_detailed/{obj.answer.question.slug}?ans_pk={obj.answer.pk}&del=2#{obj.answer.pk}'>{link}</a>")
        else:
            return None
    reason_link.short_description = "reason link"
    

@admin.register(Audio_answer)
class Audio_answer_Admin(admin.ModelAdmin):
    search_fields = ['author__username','author__email','pk', 'subtitles']
    list_display = ['author','vote_count' ,'time_created','question']
    autocomplete_fields = ['author', 'question']
        
        
@admin.register(Question_vote)
class Question_vote_Admin(admin.ModelAdmin):
    search_fields = ['question_id__title','user_id__username']
    list_display = ['question_id','user_id' ,'created','vote_type']
    autocomplete_fields = ['question_id', 'user_id']


@admin.register(Answer_vote)
class Answer_vote_Admin(admin.ModelAdmin):
    search_fields = ['audio_answer_id__question__title','user_id__username']
    list_display = ['audio_answer_id','user_id' ,'time_created','vote_type']
    autocomplete_fields = ['audio_answer_id', 'user_id']
    
    
@admin.register(Theme_vote)
class Theme_vote_Admin(admin.ModelAdmin):
    search_fields = ['theme_id__title','user_id__username']
    list_display = ['theme_id','user_id' ,'created','vote_type']
    autocomplete_fields = ['theme_id', 'user_id']


@admin.register(Reputation)
class Reputation_Admin(admin.ModelAdmin):
    search_fields = ['reciever__username','sender__username']
    list_display = ['amount','reciever' ,'sender','type']
    autocomplete_fields = ['reciever','sender', 'answer','question','theme']
    
    
@admin.register(Config)
class Reputation_Admin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    
    