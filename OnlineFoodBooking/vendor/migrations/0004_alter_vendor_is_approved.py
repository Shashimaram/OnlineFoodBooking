# Generated by Django 4.2.3 on 2023-09-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_alter_vendor_vendor_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='is_approved',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]