# Generated by Django 3.1.2 on 2020-10-11 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201011_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlink',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
            preserve_default=False,
        ),
    ]