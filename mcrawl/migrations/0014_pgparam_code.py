# Generated by Django 3.2.4 on 2021-06-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcrawl', '0013_pgparam_prevtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='pgparam',
            name='code',
            field=models.IntegerField(null=True),
        ),
    ]
