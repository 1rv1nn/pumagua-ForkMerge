# Generated by Django 4.1.6 on 2024-05-30 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pumaguaAPP', '0003_remove_bebederos_disponibilidad_reporte'),
    ]

    operations = [
        migrations.AddField(
            model_name='bebederos',
            name='estado_bebedero',
            field=models.CharField(choices=[('0', 'No disponible'), ('1', 'Disponible'), ('2', 'En mantenimiento')], default='1', help_text='EstadoBebeder', max_length=1),
        ),
    ]
