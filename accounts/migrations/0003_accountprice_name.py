# Generated by Django 4.0.5 on 2023-07-26 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_accountprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprice',
            name='name',
            field=models.CharField(default='Обліковий запис', max_length=50),
        ),
    ]