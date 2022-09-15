from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import PrependedText, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Fieldset, Column, Field, HTML
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from .custom_layout_object import *

from django.utils.translation import gettext_lazy as _

from .models import *


class FilesForm(ModelForm):
    class Meta:
        model = Files
        exclude = ('oks',)
        fields = ['file_url', 'oks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_show_labels = False


class PremisesForm(ModelForm):
    class Meta:
        model = Premises
        exclude = ()
        fields = ['cad_num', 'oks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_show_labels = False



class NoteForm(ModelForm):
    class Meta:
        model = Note
        exclude = ()
        fields = ['note', 'oks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].widget.attrs = {'rows': 3}
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Field('note', rows='3'),
        )


class AddTipForm(forms.Form):
    name = forms.CharField(max_length=40)


class AddFiles(forms.Form):
    nameFile = forms.FileField(label='Файл')


class AddOKsForm(forms.Form):
    cad_num = forms.CharField(max_length=40, label='Кадастровый номер',
                              widget=forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}))
    can_num_lend = forms.CharField(max_length=40, label='Кад. номер земельного уч.', required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}))
    adr_oks = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 60, 'row': 10, 'placeholder': 'Ввод', 'class': 'field-long field-textarea'}),
        label='Адрес объекта')
    tip_oks = forms.ModelChoiceField(queryset=Tip.objects.all(), label='Тип объекта', empty_label='Тип не выбран',
                                     widget=forms.Select(attrs={'class': 'field-select'}))


class AddOKsForm2(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tip_oks'].empty_label = 'Тип не выбран'

    class Meta:
        model = Oks
        fields = '__all__'
        widgets = {
            'cad_num': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'can_num_lend': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'adr_oks': forms.Textarea(
                attrs={'cols': 60, 'row': 2, 'placeholder': 'Ввод', 'class': 'field-long field-textarea'}),
            'tip_oks': forms.Select(attrs={'class': 'field-select'}),
            'area': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'floors': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'purpose': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'naim': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'land_purpose': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'land_area': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'cost': forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}),
            'right': forms.Textarea(
                attrs={'cols': 60, 'row': 2, 'placeholder': 'Ввод', 'class': 'field-long field-textarea'}),
        }


class TestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tip_oks'].empty_label = 'Тип не выбран'
        self.helper = FormHelper()
        self.helper.form_class = 'form-control-sm'
        self.helper.label_class = 'floatingInput'
        self.helper.field_class = 'form-control-sm'
        self.helper.form_tag=False
        self.helper.layout = Layout(
            FloatingField("cad_num"),
            FloatingField('tip_oks'),
            TabHolder(
                Tab('Данные объекта',
                    FloatingField("adr_oks"),
                    Row(
                        Column(FloatingField("area")),
                        Column(FloatingField("floors")),
                        Column(FloatingField("cost")),
                        css_class='form-row'
                    ),
                    FloatingField("naim"),
                    FloatingField("purpose"),
                    ),
                Tab('Земля',
                    FloatingField("cad_num_land"),
                    Row(
                        Column(FloatingField("land_purpose")),
                        Column(FloatingField("land_area")),
                        css_class='form-row'
                    ),
                    ),
                Tab('Права',
                    Field('right', rows='3'),
                    ),
                Tab('Помещения',
                    HTML('<div class="row">    <div class="col-10">Кадастровый номер </div>    <div class="col-sm"> </div>    </div>'),
                    Formset('premises'),
                    ),
                Tab('Заметки',
                    HTML('<div class="row">    <div class="col-10">Текст заметки </div>    <div class="col-sm"> </div>    </div>'),
                    Formset('note'),
                    ),
                Tab('Файлы',
                    HTML('<div class="row">    <div class="col-10">Файлы </div>    <div class="col-sm"> </div>    </div>'),
                    Formset('files'),
                    ),
            ),
        )

    class Meta:
        model = Oks
        fields = '__all__'


class OksFilterForm(forms.Form):
    Years = Year.objects.values_list('id', 'name')
    year_per_id = forms.ChoiceField(choices=(*Years,), label="Год перечня", required=False)


class YearForm(ModelForm):
    class Meta:
        model = Year
        exclude = ()


class PerForm(ModelForm):
    class Meta:
        model = Per
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oks'].empty_label = None
        #self.fields['oks'].widget.attrs['disabled'] = True
        self.fields['year_per'].empty_label = 'Перечень не выбран'
        self.helper = FormHelper()
        self.helper.form_class = 'form-control-sm'
        self.helper.label_class = 'floatingInput'
        self.helper.field_class = 'form-control-sm'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            FloatingField("oks"),
            FloatingField('year_per'),

            Submit('submit', 'Сохранить'),
        )


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Ввод', 'class': 'field-long'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control-sm'
        self.helper.label_class = 'floatingInput'
        self.helper.field_class = 'form-control-sm'
        self.helper.form_tag=True
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            Submit('submit', 'Войти'),
        )


OKsPremisesFormSet = inlineformset_factory(
    Oks, Premises, form=PremisesForm, extra=1, can_delete=True
)

OKsFilesFormSet = inlineformset_factory(
    Oks, Files, form=FilesForm, extra=1, can_delete=True
)

OKsNoteFormSet = inlineformset_factory(
    Oks, Note, form=NoteForm, extra=1, can_delete=True
)

OKsInlineFormSet = inlineformset_factory(Oks, Files, fields='__all__', extra=1, can_delete=True)


PerFormSet = inlineformset_factory(
    Year, Per, form=PerForm, extra=1)