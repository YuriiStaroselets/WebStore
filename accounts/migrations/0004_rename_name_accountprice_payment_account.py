# Generated by Django 4.0.5 on 2023-07-26 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_accountprice_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountprice',
            old_name='name',
            new_name='payment_account',
        ),
    ]
