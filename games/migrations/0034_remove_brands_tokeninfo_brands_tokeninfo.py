# Generated by Django 5.1.4 on 2025-01-06 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0033_brands_tokeninfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brands',
            name='tokenInfo',
        ),
        migrations.AddField(
            model_name='brands',
            name='tokenInfo',
            field=models.ManyToManyField(blank=True, to='games.tokeninfo'),
        ),
    ]
