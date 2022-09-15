import re

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from django.core.exceptions import ValidationError
from import_export.widgets import ForeignKeyWidget

from .models import *


class FileInLine(admin.TabularInline):
    model = Files
    extra = 0


class PremisesInLine(admin.TabularInline):
    model = Premises
    extra = 0


class NoteInLine(admin.TabularInline):
    model = Note
    extra = 0


class OksResource(resources.ModelResource):
    tip_oks = Field(
        column_name='tip_oks',
        attribute='tip_oks',
        widget=ForeignKeyWidget(Tip, 'name'))

    class Meta:
        model = Oks
        exclude = ('id',)
        import_id_fields = ['cad_num']


class OksAdmin(ImportExportModelAdmin):

    def oks_files_count(self, obj):
        return obj.files_set.count()

    def premises_files_count(self, obj):
        return obj.premises_set.count()

    oks_files_count.short_description = "Файлов"
    premises_files_count.short_description = "Помещений"

    list_display = ('cad_num', 'adr_oks', 'tip_oks', 'oks_files_count', 'premises_files_count')
    list_display_links = ('cad_num',)
    search_fields = ('cad_num',)
    list_filter = ('tip_oks',)
    inlines = [FileInLine, PremisesInLine, NoteInLine]
    fields = ('cad_num', 'adr_oks', 'tip_oks', 'area', 'cad_num_land', 'land_purpose', 'land_area',
         'floors', 'purpose', 'naim', 'cost', 'right')
    list_per_page = 100
    save_on_top = True
    resource_class = OksResource


admin.site.register(Oks, OksAdmin)


class TipAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Tip, TipAdmin)


class YearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Year, YearAdmin)


class PremisesResource(resources.ModelResource):
    oks = Field(
        column_name='oks',
        attribute='oks',
        widget=ForeignKeyWidget(Oks, 'cad_num'))

    class Meta:
        model = Premises
        exclude = ('id',)
        import_id_fields = ['cad_num']


class PremisesAdmin(ImportExportModelAdmin):
    list_display = ('cad_num', 'oks')
    list_display_links = ('cad_num', 'oks')
    search_fields = ('cad_num', )
    list_per_page = 100
    resource_class = PremisesResource


admin.site.register(Premises, PremisesAdmin)


class NoteResource(resources.ModelResource):
    oks = Field(
        column_name='oks',
        attribute='oks',
        widget=ForeignKeyWidget(Oks, 'cad_num'))

    class Meta:
        model = Note
        exclude = ('id',)
        import_id_fields = ['cad_num']


class NoteAdmin(ImportExportModelAdmin):
    list_display = ('note', 'oks')
    list_display_links = ('note', 'oks')
    search_fields = ('oks', )
    list_per_page = 100
    resource_class = NoteResource


admin.site.register(Note, NoteAdmin)


class PerResource(resources.ModelResource):
    oks = Field(
        column_name='oks',
        attribute='oks',
        widget=ForeignKeyWidget(Oks, 'cad_num'))
    year_per = Field(
        column_name='year_per',
        attribute='year_per',
        widget=ForeignKeyWidget(Year, 'name'))

    class Meta:
        model = Per
        exclude = ('id',)
        import_id_fields = ['oks']


class PerAdmin(ImportExportModelAdmin):

    def get_oks_adr(self, obj):
        return obj.oks.adr_oks

    def get_oks_tip(self, obj):
        return obj.oks.tip_oks

    get_oks_adr.short_description = "Адрес"
    get_oks_tip.short_description = "Тип"

    list_display = ('oks', 'get_oks_adr', 'get_oks_tip', 'year_per')
    list_display_links = ('oks',)
    search_fields = ('oks__cad_num', 'oks__adr_oks')
    list_filter = ('year_per', )
    list_per_page = 100
    resource_class = PerResource


admin.site.register(Per, PerAdmin)


class FilesAdmin(admin.ModelAdmin):
    list_display = ('file_url', 'oks')
    list_display_links = ('file_url',)
    search_fields = ('file_url', 'oks')


admin.site.register(Files, FilesAdmin)

admin.site.site_title = 'Админ-панель Перечень Кузбасса'
admin.site.site_header = 'Админ-панель Перечень Кузбасса'