# Generated by Django 3.1.4 on 2021-02-01 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('domain', models.URLField()),
                ('options', models.CharField(max_length=800)),
                ('order_id', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='mainsite.customers')),
            ],
            options={
                'db_table': 'order',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('options', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='mainsite.customers')),
            ],
            options={
                'db_table': 'cart',
                'ordering': ['created', 'updated'],
            },
        ),
        migrations.CreateModel(
            name='ActiveProjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_projects', to='mainsite.customers')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='sales.orders')),
            ],
            options={
                'db_table': 'active_projects',
                'ordering': ['created'],
            },
        ),
    ]
