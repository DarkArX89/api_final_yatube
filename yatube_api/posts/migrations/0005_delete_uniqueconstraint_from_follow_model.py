# Generated by Django 3.2.16 on 2023-03-13 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_follow_model_edit'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_follow',
        ),
    ]
