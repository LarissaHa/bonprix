# Generated by Django 2.0.10 on 2019-04-18 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20190208_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='product_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reviews.Product'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reviews.Review'),
        ),
    ]
