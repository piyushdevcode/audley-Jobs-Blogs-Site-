# Generated by Django 3.2.9 on 2021-12-08 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_recieved_on_feedback_received_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ['-received_on']},
        ),
    ]
