# Generated by Django 2.1.7 on 2019-02-18 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_videomodel_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videomodel',
            old_name='public',
            new_name='public_access',
        ),
    ]
