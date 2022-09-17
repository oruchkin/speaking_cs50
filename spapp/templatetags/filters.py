import hashlib
from django.template.defaulttags import register
from django.urls import reverse

# TEMPLATE USE: {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=315):
    hash = (hashlib.md5(email.encode('utf-8').lower()).hexdigest())
    return f"https://www.gravatar.com/avatar/{hash}?s={size}&d=identicon&r=PG" 


@register.filter
def profile_reputation_title(reputation_obj):
    if reputation_obj.answer:
        result = reputation_obj.answer.subtitles
        if len(result) > 27:
            result = result[0:25] + "..."
        return result
    elif reputation_obj.question:
        result = reputation_obj.question.title
        if len(result) > 27:
            result = result[0:25] + "..."
        return result
    elif reputation_obj.theme:
        result = reputation_obj.theme.title
        if len(result) > 27:
            result = result[0:25] + "..."
        return result
    else:
        return False
    
@register.filter
def profile_reputation_link(reputation_obj):
    if reputation_obj.answer:
        answer_obj = reputation_obj.answer
        question_slug = reputation_obj.answer.question.slug
        return reverse("question_detailed", args=[question_slug])+f"#{answer_obj.pk}"
    elif reputation_obj.question:
        question_obj = reputation_obj.question
        return reverse("theme_detailed", args=[question_obj.theme.slug])+f"#share-dialog-blok-{question_obj.pk}"
    elif reputation_obj.theme:
        theme_obj = reputation_obj.theme
        return reverse("theme_detailed", args=[theme_obj.slug])
    else:
        return False
    
    