# Generated by Django 4.0.1 on 2022-04-26 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_request_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
