# Generated by Django 4.0.4 on 2022-12-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema', models.CharField(max_length=100, verbose_name='Название')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('type', models.CharField(max_length=100, verbose_name='Тип')),
                ('rs_definition', models.CharField(max_length=300, verbose_name='РС-определение')),
                ('term', models.CharField(max_length=500, verbose_name='Термин')),
                ('text_definition', models.TextField(verbose_name='Текстовое определение')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
