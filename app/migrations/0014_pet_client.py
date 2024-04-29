# Generated by Django 5.0.4 on 2024-04-28 21:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_pet_vets'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='client',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='app.client'),
            preserve_default=False,
        ),
    ]
