# Generated by Django 5.0 on 2024-01-12 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_user_refer_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='refer_by',
            field=models.CharField(default='admin', max_length=100),
        ),
    ]
