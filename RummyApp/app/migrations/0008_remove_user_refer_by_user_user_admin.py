# Generated by Django 5.0 on 2024-01-18 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_referlinksender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='refer_by',
        ),
        migrations.AddField(
            model_name='user',
            name='user_admin',
            field=models.CharField(default='12:59', max_length=100),
            preserve_default=False,
        ),
    ]
