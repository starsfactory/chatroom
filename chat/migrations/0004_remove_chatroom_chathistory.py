# Generated by Django 4.2.10 on 2024-03-04 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_groupnumber_remove_chatroom_groupuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='chathistory',
        ),
    ]
