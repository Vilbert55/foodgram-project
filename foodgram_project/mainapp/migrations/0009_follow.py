# Generated by Django 3.1.2 on 2020-11-07 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0008_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumer', to=settings.AUTH_USER_MODEL)),
                ('cook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cook', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
