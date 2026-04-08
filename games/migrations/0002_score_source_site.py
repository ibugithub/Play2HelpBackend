from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='source_site',
            field=models.CharField(
                choices=[
                    ('unknown', 'Unknown'),
                    ('weplay2help', 'WePlay2Help'),
                    ('weplay2health', 'WePlay2Health'),
                    ('weplay2learn', 'WePlay2Learn'),
                    ('weplay2love', 'WePlay2Love'),
                    ('weplay2work', 'WePlay2Work'),
                ],
                db_index=True,
                default='unknown',
                max_length=30,
            ),
        ),
        migrations.AddIndex(
            model_name='score',
            index=models.Index(fields=['user', 'game', 'source_site'], name='games_score_user_id_e63d8c_idx'),
        ),
    ]
