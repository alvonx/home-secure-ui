# Generated by Django 4.1.7 on 2023-03-23 09:28

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                default=django.utils.timezone.now, upload_to="blogpost/"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="post",
            name="body",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
