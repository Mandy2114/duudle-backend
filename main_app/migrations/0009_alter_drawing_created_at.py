# Generated by Django 5.1.3 on 2024-11-20 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_drawing_options_drawing_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
