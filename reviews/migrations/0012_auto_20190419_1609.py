# Generated by Django 2.0.10 on 2019-04-19 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20190418_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='prodcut',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='review',
            name='product_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reviews.Product'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='reviews.Product'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reviews.Review'),
        ),
    ]
