# Generated by Django 5.0.6 on 2024-09-28 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.BigIntegerField(default=0, verbose_name='Баланс'),
        ),
    ]