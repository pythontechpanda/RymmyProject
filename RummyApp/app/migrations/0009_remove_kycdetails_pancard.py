# Generated by Django 5.0 on 2024-01-18 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_user_refer_by_user_user_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kycdetails',
            name='pancard',
        ),
    ]
