# Generated by Django 4.1.3 on 2022-11-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("url", "0002_rename_shortened_url_url_shorten_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="url",
            name="pub_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
