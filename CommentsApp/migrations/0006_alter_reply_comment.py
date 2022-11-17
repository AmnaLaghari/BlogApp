# Generated by Django 4.1.3 on 2022-11-17 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CommentsApp', '0005_alter_comment_likes_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='CommentsApp.comment'),
        ),
    ]
