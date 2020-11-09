# Generated by Django 3.1.2 on 2020-11-09 07:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0010_auto_20201109_0947'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'recipe')},
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('consumer', 'cook')},
        ),
    ]
