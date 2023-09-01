# Generated by Django 4.2.3 on 2023-09-01 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_2',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
