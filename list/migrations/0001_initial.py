# Generated by Django 4.1.1 on 2022-09-06 12:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import list.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cad_num', models.CharField(max_length=40, unique=True, validators=[list.models.validate_cad_num], verbose_name='Кадастровый номер')),
                ('cad_num_land', models.CharField(blank=True, max_length=40, null=True, validators=[list.models.validate_cad_num], verbose_name='Кад номер земельного участка')),
                ('adr_oks', models.TextField(blank=True, null=True, verbose_name='Адрес объекта')),
                ('adr_oks_sort', models.TextField(blank=True, null=True, verbose_name='Адрес объекта для сортировки')),
                ('area', models.CharField(blank=True, max_length=20, null=True, verbose_name='Площадь м2')),
                ('floors', models.CharField(blank=True, max_length=20, null=True, verbose_name='Этажность')),
                ('purpose', models.CharField(blank=True, max_length=255, null=True, verbose_name='Использование')),
                ('naim', models.CharField(blank=True, max_length=255, null=True, verbose_name='Наименование')),
                ('land_purpose', models.TextField(blank=True, null=True, verbose_name='Использование зем. уч.')),
                ('land_area', models.CharField(blank=True, max_length=20, null=True, verbose_name='Площадь зем. уч.')),
                ('cost', models.CharField(blank=True, max_length=30, null=True, verbose_name='Стоимость')),
                ('right', models.TextField(blank=True, null=True, verbose_name='Права')),
            ],
            options={
                'verbose_name': 'Объект перечня',
                'verbose_name_plural': 'Объекты перечня',
                'ordering': ['adr_oks'],
            },
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, verbose_name='Имя типа объекта')),
            ],
            options={
                'verbose_name': 'Тип объектов',
                'verbose_name_plural': 'Типы объектов',
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(verbose_name='Год')),
            ],
            options={
                'verbose_name': 'Год перечня',
                'verbose_name_plural': 'Годы перечня',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Premises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cad_num', models.CharField(blank=True, max_length=40, validators=[list.models.validate_cad_num], verbose_name='Кадастровый номер')),
                ('oks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.oks', verbose_name='Кад номер здания')),
            ],
            options={
                'verbose_name': 'Помещение в здании',
                'verbose_name_plural': 'Помещения в здании',
            },
        ),
        migrations.CreateModel(
            name='Per',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.oks', verbose_name='№ объекта')),
                ('year_per', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.year', verbose_name='Год перечня')),
            ],
            options={
                'verbose_name': 'Перечнь',
                'verbose_name_plural': 'Перечни',
                'ordering': ['year_per'],
            },
        ),
        migrations.AddField(
            model_name='oks',
            name='tip_oks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='list.tip', verbose_name='Тип объекта'),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='Заметка')),
                ('oks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.oks', verbose_name='Кад номер здания')),
            ],
            options={
                'verbose_name': 'Заметка',
                'verbose_name_plural': 'Заметки',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.FileField(blank=True, upload_to=list.models.content_file_name, validators=[django.core.validators.FileExtensionValidator(['pdf', 'txt', 'doc', 'xml', 'docx'])], verbose_name='Файл')),
                ('oks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.oks', verbose_name='Кад номер здания')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
    ]
