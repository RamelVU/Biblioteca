# Generated by Django 3.0.4 on 2021-01-10 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0002_auto_20210105_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='fecha_creacion',
            field=models.DateField(auto_now=True, verbose_name='Fecha de creación'),
        ),
    ]
