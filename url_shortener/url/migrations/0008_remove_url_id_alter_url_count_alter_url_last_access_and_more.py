# Generated by Django 4.1.3 on 2022-11-09 22:43

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import re


class Migration(migrations.Migration):

    dependencies = [
        ("url", "0007_url_last_access"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="url",
            name="id",
        ),
        migrations.AlterField(
            model_name="url",
            name="count",
            field=models.IntegerField(default=0, verbose_name="Number of accesses"),
        ),
        migrations.AlterField(
            model_name="url",
            name="last_access",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Last access date"
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="original_url",
            field=models.URLField(
                help_text="Enter the URL you want to shorten",
                max_length=250,
                validators=[
                    django.core.validators.URLValidator,
                    django.core.validators.MinLengthValidator(2),
                ],
                verbose_name="Original URL",
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="pub_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Publication date"
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="shorten_url",
            field=models.SlugField(
                max_length=5,
                primary_key=True,
                serialize=False,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                        "invalid",
                    )
                ],
                verbose_name="Shorten URL slug",
            ),
        ),
    ]
