import re

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


# Create your models here.


class Tip(models.Model):
    name = models.CharField(max_length=40, blank=True, verbose_name="Имя типа объекта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип объектов'
        verbose_name_plural = 'Типы объектов'

    def get_absolute_url(self):
        return reverse('tip', kwargs={'tip_id': self.pk})


class Year(models.Model):
    name = models.IntegerField(verbose_name="Год")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Год перечня'
        verbose_name_plural = 'Годы перечня'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('year', kwargs={'year_id': self.pk})


def content_file_name(instance, filename):
    obj_name = instance.oks.cad_num.replace(':', '')
    return '/'.join([obj_name, filename])


def validate_cad_num(value):
    if re.findall(r'^(\d{2}):?(\d{2}):?(\d{7}):?(\d*)$', value):
        return value
    else:
        raise ValidationError('Формат кадастрового номера 00:00:0000000:00+')


def validate_file_name(value):
    if re.findall(r'^(.*?)\.(xml|pdf|doc|docx|txt)$', value):
        return value
    else:
        raise ValidationError('Тип файла не поддерживается')


def convert_to_zero(match_obj):
    return str(match_obj.group().zfill(3))


class Oks(models.Model):
    cad_num = models.CharField(max_length=40, blank=False, null=False, unique=True, verbose_name="Кадастровый номер",
                               validators=[validate_cad_num])
    cad_num_land = models.CharField(max_length=40, blank=True, null=True, verbose_name="Кад номер земельного участка",
                                    validators=[validate_cad_num])
    adr_oks = models.TextField(blank=False, null=False, verbose_name="Адрес объекта")
    adr_oks_sort = models.TextField(blank=True, null=True, verbose_name="Адрес объекта для сортировки")
    tip_oks = models.ForeignKey(Tip, on_delete=models.PROTECT, verbose_name="Тип объекта")
    area = models.CharField(max_length=20, blank=True, null=True, verbose_name="Площадь м2")
    floors = models.CharField(max_length=20, blank=True, null=True, verbose_name="Этажность")
    purpose = models.CharField(max_length=255, blank=True, null=True, verbose_name="Использование")
    naim = models.CharField(max_length=255, blank=True, null=True, verbose_name="Наименование")
    land_purpose = models.TextField(blank=True, null=True, verbose_name="Использование зем. уч.")
    land_area = models.CharField(max_length=20, blank=True, null=True, verbose_name="Площадь зем. уч.")
    cost = models.CharField(max_length=30, blank=True, null=True, verbose_name="Стоимость")
    right = models.TextField(blank=True, null=True, verbose_name="Права")

    def __str__(self):
        return self.cad_num

    def get_absolute_url(self):
        return reverse('oks_update', kwargs={'pk': self.pk})

    def num_files(self):
        return self.files_set.count()

    def num_premises(self):
        return self.premises_set.count()

    def save(self, *args, **kwargs):
        if self.adr_oks != '':
            self.adr_oks_sort = re.sub(r'\d+', convert_to_zero, self.adr_oks)
            print(self.adr_oks_sort)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Объект перечня'
        verbose_name_plural = 'Объекты перечня'
        ordering = ['adr_oks']


class Files(models.Model):
    file_url = models.FileField(upload_to=content_file_name, blank=True, verbose_name="Файл",
                                validators=[FileExtensionValidator(['pdf', 'txt', 'doc', 'xml', 'docx'])])
    oks = models.ForeignKey(Oks, on_delete=models.CASCADE, verbose_name="Кад номер здания")

    def __str__(self):
        return str(self.file_url)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'


class Premises(models.Model):
    cad_num = models.CharField(max_length=40, blank=True, verbose_name="Кадастровый номер",
                               validators=[validate_cad_num])
    oks = models.ForeignKey(Oks, on_delete=models.CASCADE, verbose_name="Кад номер здания")

    def __str__(self):
        return self.cad_num

    class Meta:
        verbose_name = 'Помещение в здании'
        verbose_name_plural = 'Помещения в здании'


class Per(models.Model):
    oks = models.ForeignKey(Oks, on_delete=models.CASCADE, verbose_name="№ объекта")
    year_per = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name="Год перечня")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Перечнь'
        verbose_name_plural = 'Перечни'
        ordering = ['year_per']


class Note(models.Model):
    note = models.TextField(blank=True, verbose_name="Заметка")
    oks = models.ForeignKey(Oks, on_delete=models.CASCADE, verbose_name="Кад номер здания")

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'