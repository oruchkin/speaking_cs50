# Generated by Django 4.0.5 on 2022-07-21 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0018_audio_answer_share_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reputation',
            field=models.IntegerField(default=0),
        ),
    ]
