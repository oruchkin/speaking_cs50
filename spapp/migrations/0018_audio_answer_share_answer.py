# Generated by Django 4.0.5 on 2022-07-19 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0017_audio_answer_vote_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio_answer',
            name='share_answer',
            field=models.BooleanField(default=True),
        ),
    ]
