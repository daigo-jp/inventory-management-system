# Generated by Django 5.1.2 on 2024-10-25 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_remove_food_description_alter_food_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
