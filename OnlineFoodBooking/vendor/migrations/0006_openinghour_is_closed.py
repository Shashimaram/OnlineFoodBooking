# Generated by Django 4.2.3 on 2023-09-18 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_openinghour'),
    ]

    operations = [
        migrations.AddField(
            model_name='openinghour',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]