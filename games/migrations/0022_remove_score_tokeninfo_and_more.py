# Generated by Django 5.1.4 on 2024-12-25 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0021_alter_tokeninfo_token_symbol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='tokenInfo',
        ),
        migrations.AlterField(
            model_name='tokeninfo',
            name='bnb_contract_address',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
    ]
