# Generated by Django 5.1.4 on 2024-12-28 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0027_alter_brands_started_date_alter_members_joined_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='earned_dollar',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='members',
            name='earned_tokens',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='members',
            name='role',
            field=models.CharField(choices=[('founder', 'Founder'), ('CEO', 'CEO'), ('devs', 'Developer'), ('product manager', 'Product Manager')], max_length=50),
        ),
    ]
