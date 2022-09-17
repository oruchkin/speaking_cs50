# Generated by Django 4.0.5 on 2022-08-24 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0026_alter_question_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('reason', models.TextField()),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spapp.audio_answer')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spapp.question')),
                ('report_reciever', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='report_reciever', to=settings.AUTH_USER_MODEL)),
                ('report_sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='report_sender', to=settings.AUTH_USER_MODEL)),
                ('theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='spapp.theme')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
