# Generated by Django 5.0.6 on 2024-06-26 03:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]