# Generated by Django 3.2.4 on 2021-06-10 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcrawl', '0014_pgparam_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pgparam',
            old_name='code',
            new_name='errcode',
        ),
    ]