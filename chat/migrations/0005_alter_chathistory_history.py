# Generated by Django 4.2.10 on 2024-03-04 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_chatroom_chathistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chathistory',
            name='history',
            field=models.CharField(max_length=20000),
        ),
    ]