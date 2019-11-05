# Generated by Django 2.2.6 on 2019-11-05 03:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='descripcion',
            field=models.CharField(default='asd', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='nombre',
            field=models.CharField(default='das', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entrada',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pago',
            name='comprobante',
            field=models.ImageField(upload_to='comprobantes/'),
        ),
    ]