# Generated by Django 4.0.1 on 2022-01-31 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_rename_shoplist_shoppingcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipes',
            field=models.ManyToManyField(related_name='shoplist', to='recipes.Recipe'),
        ),
    ]
