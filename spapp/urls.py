from django.urls import path


from . import views, views_auth, views_profile,views_answer, views_question, views_theme, views_rating

urlpatterns = [
    # authentication
    path("login/", views_auth.login_view, name="login"),
    path("logout/", views_auth.logout_view, name="logout"),
    path("register/", views_auth.register, name="register"),  
    # .html pages
    path("", views.index, name='index'),
    path("theme_detailed/<slug:theme_slug>", views_theme.theme_detailed, name='theme_detailed'),
    path("question_detailed/<slug:q_slug>", views_question.question_detailed, name='question_detailed'),
    path("new_audio_answer/<slug:q_slug>", views.new_audio_answer, name='new_audio_answer'),
    path("delete_answer/<int:answer_pk>", views.delete_answer, name='delete_answer'),
    
    # .rating
    path("rating_user/", views_rating.rating_user, name='rating_user'),
    path("rating_theme/", views_rating.rating_theme, name='rating_theme'),
    path("rating_question/", views_rating.rating_question, name='rating_question'),
    path("rating_answer/", views_rating.rating_answer, name='rating_answer'),
    
    # .profile
    path("profile/<int:user_pk>", views_profile.profile, name='profile'),
    path("profile_answers/<int:user_pk>", views_profile.profile_answers, name='profile_answers'),
    path("profile_questions/<int:user_pk>", views_profile.profile_questions, name='profile_questions'),
    path("profile_theme/<int:user_pk>", views_profile.profile_theme, name='profile_theme'),
    path("profile_reputation/<int:user_pk>", views_profile.profile_reputation, name='profile_reputation'),
    
    # logic
    path("subtitle_generator/", views_answer.subtitle_generator, name='subtitle_generator'),
    path("save_audio_answer/", views_answer.save_audio_answer, name='save_audio_answer'),
    # ajax_answer
    path("ajax/answer/upvote/", views_answer.upvote_answer),
    path("ajax/answer/downvote/", views_answer.downvote_answer),
    path("ajax/share_answer/", views_answer.ajax_share_answer),
    # ajax question
    path("ajax/question/upvote/", views_question.upvote_question),
    path("ajax/question/downvote/", views_question.downvote_question),
    # ajax theme
    path("ajax/theme/upvote/", views_theme.upvote_theme),
    path("ajax/theme/downvote/", views_theme.downvote_theme),
    
    
]


