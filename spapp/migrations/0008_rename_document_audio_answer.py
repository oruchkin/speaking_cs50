# Generated by Django 4.0.5 on 2022-07-03 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0007_question_slug_alter_theme_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Document',
            new_name='Audio_answer',
        ),
    ]
