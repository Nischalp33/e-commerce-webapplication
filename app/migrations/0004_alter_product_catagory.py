# Generated by Django 4.0.1 on 2022-03-03 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_ststus_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='catagory',
            field=models.CharField(choices=[('G', 'Gaming'), ('A', 'Apple'), ('C', 'Accessories')], max_length=2),
        ),
    ]
