# Generated by Django 3.1.4 on 2021-02-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_payid_pay_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='options',
        ),
        migrations.AddField(
            model_name='orders',
            name='options_name',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='options_price',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
