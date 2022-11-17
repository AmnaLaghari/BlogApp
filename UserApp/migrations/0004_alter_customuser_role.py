# Generated by Django 4.1.3 on 2022-11-11 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0003_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'User'), (2, 'Moderator')], null=True),
        ),
    ]
