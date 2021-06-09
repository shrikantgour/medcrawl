# Generated by Django 3.2.4 on 2021-06-08 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='paged',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pgno', models.CharField(max_length=5)),
                ('title', models.CharField(max_length=150)),
                ('read', models.CharField(max_length=20)),
                ('dt', models.CharField(max_length=12)),
                ('gdt', models.CharField(max_length=22)),
                ('link', models.CharField(max_length=150)),
                ('tags', models.CharField(max_length=150)),
            ],
        ),
    ]
