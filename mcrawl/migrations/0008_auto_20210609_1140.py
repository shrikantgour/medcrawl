# Generated by Django 3.2.4 on 2021-06-09 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcrawl', '0007_delete_pagedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='paged',
            name='bgauthor',
            field=models.CharField(default='NA', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paged',
            name='bglink',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='paged',
            name='bgpage',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
