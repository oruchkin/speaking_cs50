# Generated by Django 4.0.5 on 2022-09-08 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0034_question_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_vote',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_id_vote', to='spapp.question'),
        ),
    ]
