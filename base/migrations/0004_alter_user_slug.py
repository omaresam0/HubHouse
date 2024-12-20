# Generated by Django 5.1.2 on 2024-11-26 20:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_alter_user_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="slug",
            field=models.SlugField(
                blank=True,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
