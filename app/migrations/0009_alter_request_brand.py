# Generated by Django 4.0.1 on 2022-04-25 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='brand',
            field=models.CharField(max_length=200),
        ),
    ]