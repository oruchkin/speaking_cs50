# Generated by Django 4.0.5 on 2022-09-08 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0035_alter_question_vote_question_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme_vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('upvote', 'upvote'), ('downvote', 'downvote')], max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('theme_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme_id_vote', to='spapp.theme')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme_user_vote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
