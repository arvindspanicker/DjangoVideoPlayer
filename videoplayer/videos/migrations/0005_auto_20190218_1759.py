# Generated by Django 2.1.7 on 2019-02-18 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20190218_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='video_file',
            field=models.FileField(upload_to='videos/'),
        ),
    ]
