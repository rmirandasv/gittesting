# Generated by Django 3.2.5 on 2021-07-14 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitwrapper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pullrequest',
            name='author',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='pullrequest',
            name='author_email',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
