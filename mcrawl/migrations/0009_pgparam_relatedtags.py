# Generated by Django 3.2.4 on 2021-06-09 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcrawl', '0008_auto_20210609_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='pgparam',
            name='relatedtags',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
