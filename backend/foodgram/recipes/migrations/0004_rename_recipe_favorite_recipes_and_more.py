# Generated by Django 4.0.1 on 2022-01-29 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_follow_unique_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='recipe',
            new_name='recipes',
        ),
        migrations.RenameField(
            model_name='shoplist',
            old_name='recipe',
            new_name='recipes',
        ),
    ]
