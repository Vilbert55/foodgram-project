# Generated by Django 3.1.2 on 2020-11-07 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='mainapp.recipe'),
            preserve_default=False,
        ),
    ]
