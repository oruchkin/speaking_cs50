# Generated by Django 4.0.5 on 2022-07-23 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0021_alter_theme_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='link',
            field=models.CharField(max_length=1000, null=True, unique=True),
        ),
    ]