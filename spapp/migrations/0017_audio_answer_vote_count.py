# Generated by Django 4.0.5 on 2022-07-17 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0016_answer_vote_time_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio_answer',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]