import os

import xlwt
import uuid
import datetime
from crispy_forms.layout import Div
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from docxtpl import DocxTemplate
import io

from kuzlist import settings
from .forms import *
from .models import *
from .utils import *
from .filters import *

import xml.etree.ElementTree as ET


# Create your views here.


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена')


class OksListView(DataMixin,  ListView):
    paginate_by = 2
    model = Per
    template_name = 'list/objtoperlist.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        years = Year.objects.all()
        filtered_per = PerFilter(
            self.request.GET,
            queryset=Per.objects.all()
        )
        context['years'] = years
        #context['year_per_id'] = int(self.request.GET.get('year_per_id'))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        form = OksFilterForm(self.request.GET)
        new_context = Per.objects.all()
        if self.request.GET.get('year_per_id'):
            new_context = Per.objects.filter(year_per_id=self.request.GET.get('year_per_id'))
        return new_context


class OksTipListView(LoginRequiredMixin, DataMixin, ListView):
    model = Oks
    template_name = 'list/tip.html'
    context_object_name = 'obj'
    allow_empty = False
    login_url = '/admin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Тип объекта - " + str(context['obj'][0].tip_oks))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Oks.objects.filter(tip_oks=self.kwargs['tip_id'])


class OksViewCreate(LoginRequiredMixin, DataMixin, CreateView):
    model = Oks
    template_name = 'list/test.html'
    success_url = '/add_to_per'
    login_url = '/admin/'
    form_class = TestForm

    def get_context_data(self, **kwargs):
        context = super(OksViewCreate, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление объекта")
        if self.request.POST:
            context["premises"] = OKsPremisesFormSet(self.request.POST)
            context["note"] = OKsNoteFormSet(self.request.POST)
            context["files"] = OKsFilesFormSet(self.request.POST, self.request.FILES)
        else:
            context["premises"] = OKsPremisesFormSet()
            context["note"] = OKsNoteFormSet()
            context["files"] = OKsFilesFormSet()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        context = self.get_context_data()
        premises = context["premises"]
        files = context["files"]
        note = context["note"]
        if form.is_valid() and premises.is_valid() and files.is_valid() and note.is_valid():
            self.object = form.save()
            premises.instance = self.object
            premises.save()
            note.instance = self.object
            note.save()
            files.instance = self.object
            files.save()
            if self.request.POST.get('add_and_per'):
                return redirect('add_to_per', pk_obj = self.object.pk)
            if self.request.POST.get('add_and_next'):
                return redirect('add_obj_inline')
        return self.render_to_response(context)


class OksViewUpdate(LoginRequiredMixin, DataMixin, UpdateView):
    model = Oks
    template_name = 'list/oks_edit.html'
    success_url = '/index'
    login_url = '/admin/'
    form_class = TestForm

    # get object

    def get_context_data(self, **kwargs):
        context = super(OksViewUpdate, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактирование объекта")
        if self.request.POST:
            context["premises"] = OKsPremisesFormSet(self.request.POST, instance=self.object)
            context["note"] = OKsNoteFormSet(self.request.POST, instance=self.object)
            context["files"] = OKsFilesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context["premises"] = OKsPremisesFormSet(instance = self.object)
            context["note"] = OKsNoteFormSet(instance = self.object)
            context["files"] = OKsFilesFormSet(instance = self.object)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        context = self.get_context_data()
        premises = context["premises"]
        files = context["files"]
        note = context["note"]
        if form.is_valid() and premises.is_valid() and files.is_valid() and note.is_valid():
            self.object = form.save()
            premises.instance = self.object
            premises.save()
            note.instance = self.object
            note.save()
            files.instance = self.object
            files.save()
            return redirect('oks_update', pk = self.object.pk)
        return self.render_to_response(context)


class ObjPerCreate(LoginRequiredMixin, DataMixin, CreateView):
    model = Per
    template_name = 'list/add_obj_to_per.html'
    login_url = '/admin/'
    #fields = "__all__"
    form_class = PerForm
    success_url = '/add_obj_inline'

    def get_context_data(self, **kwargs):
        context = super(ObjPerCreate, self).get_context_data(**kwargs)

        c_def = self.get_user_context(title="Добавление объекта")
        context['pk_obj'] = self.kwargs['pk_obj']
        return dict(list(context.items()) + list(c_def.items()))

    def get_form(self, *args, **kwargs):
        form = super(ObjPerCreate, self).get_form(*args, **kwargs)
        form.fields['oks'].queryset = form.fields['oks'].queryset.filter(id=self.kwargs['pk_obj'])
        return form


class TipListView(LoginRequiredMixin, DataMixin, ListView):
    model = Tip
    template_name = 'list/tips.html'
    context_object_name = 'tips'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Типы")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Tip.objects.annotate(Count('oks'))


class PerListView(LoginRequiredMixin, DataMixin, ListView):
    model = Per
    template_name = 'list/perlist.html'
    context_object_name = 'obj'
    allow_empty = False
    login_url = '/admin/'

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('delete'):
            Per.objects.filter(id__in=self.request.POST.getlist('item')).delete()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        data = self.request.GET.copy()
        if 'year_per' not in data:
            q = Year.objects.all().order_by('-id')
            if q.count() > 0:
                data['year_per'] = q.values('id')[0]['id']
        filtered_per = PerFilter(
            data,
            queryset=Per.objects.order_by('oks__adr_oks_sort')
        )
        filtered_per.helper = FormHelper()
        filtered_per.helper.form_show_labels = True
        filtered_per.helper.form_tag = False
        filtered_per.helper.layout = Layout(
            Field('year_per', css_class="form-select-sm"),
            Field('oks__tip_oks', css_class="form-select-sm"),
            Field('q', placeholder="Введите значение", css_class="form-select-sm"),
        )
        paginated_filtered_per = Paginator(filtered_per.qs, 100)
        page_number = self.request.GET.get('page')
        page_obj = paginated_filtered_per.get_page(page_number)

        c_def = self.get_user_context(title="Главная страница",
            filtered_per = filtered_per,
            page_obj = page_obj,
        )

        return dict(list(context.items()) + list(c_def.items()))


class PerListGestView(DataMixin, ListView):
    model = Per
    template_name = 'list/pergestlist.html'
    context_object_name = 'obj'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.request.GET.copy()
        if 'year_per' not in data:
            q = Year.objects.all().order_by('-id')
            if q.count() > 0:
                data['year_per'] = q.values('id')[0]['id']
        filtered_per = PerFilter(
            data,
            queryset=Per.objects.order_by('oks__adr_oks_sort')
        )
        filtered_per.helper = FormHelper()
        filtered_per.helper.form_show_labels = True
        filtered_per.helper.form_tag = False
        filtered_per.helper.layout = Layout(
            Field('year_per', css_class="form-select-sm"),
            Field('oks__tip_oks', css_class="form-select-sm"),
            Field('q', placeholder="Введите значение", css_class="form-select-sm"),
        )
        paginated_filtered_per = Paginator(filtered_per.qs, 100)
        page_number = self.request.GET.get('page')
        page_obj = paginated_filtered_per.get_page(page_number)

        c_def = self.get_user_context(title="Главная страница",
            filtered_per = filtered_per,
            page_obj = page_obj,
        )

        return dict(list(context.items()) + list(c_def.items()))


class ObjsAddToPerListView(LoginRequiredMixin, DataMixin, ListView):
    model = Oks
    template_name = 'list/objtoperlist.html'
    context_object_name = 'obj'
    allow_empty = False
    login_url = '/admin/'

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('add'):
            items = self.request.POST.getlist('item')
            year = self.request.POST.get('year_per')
            for item in items:
                b = Per.objects.create(oks_id=int(item), year_per_id=int(year))
                b.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        data = self.request.GET.copy()
        if 'year_per' not in data:
            q = Year.objects.all().order_by('-id')
            if q.count() > 0:
                data['year_per'] = q.values('id')[0]['id']
        filtered_per = OksFilter(
            data,
            queryset=Oks.objects.order_by('adr_oks_sort')
        )

        filtered_per.helper = FormHelper()
        filtered_per.helper.form_show_labels = True
        filtered_per.helper.form_tag = False
        filtered_per.helper.layout = Layout(
            Field('per__year_per', css_class="form-select-sm"),
            Field('tip_oks', css_class="form-select-sm"),
            Field('q', placeholder="Введите значение", css_class="form-select-sm"),
        )
        paginated_filtered_per = Paginator(filtered_per.qs, 100)
        page_number = self.request.GET.get('page')
        page_obj = paginated_filtered_per.get_page(page_number)
        years = Year.objects.values_list('id', 'name')

        c_def = self.get_user_context(title="Добавление объектов в перечень",
            filtered_per = filtered_per,
            page_obj = page_obj,
            years = years,
            year_per = int(data['year_per'])
        )

        return dict(list(context.items()) + list(c_def.items()))


@login_required(login_url='/admin/')
def index(request):

    filtered_per = PerFilter(
        request.GET,
        queryset=Per.objects.order_by('oks__adr_oks_sort')
    )
    filtered_per.helper = FormHelper()
    filtered_per.helper.form_show_labels = True
    filtered_per.helper.form_tag = False
    filtered_per.helper.layout = Layout(
            Field('year_per', css_class="form-select-sm"),
            Field('oks__tip_oks', css_class="form-select-sm"),
            Field('q', placeholder="Введите значение", css_class="form-select-sm"),
    )
    paginated_filtered_per = Paginator(filtered_per.qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered_per.get_page(page_number)

    context = {
        'title': "Главная страница",
        'filtered_per': filtered_per,
        'page_obj': page_obj,
        'user_is_login': request.user.is_authenticated,
    }

    return render(request, 'list/index.html', context=context)


def handle_uploaded_file(f):
    with open('/files/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/admin/')
def add_tip(request):
    if request.method == 'POST':
        form = AddOKsForm(request.POST)
        form2 = AddFiles(request.POST, request.FILES)

        if form.is_valid():
            try:
                Oks.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления Объекта')

        if form2.is_valid():
            root = ET.parse(request.FILES['nameFile'])
            cn = root.findall(".//build_record//object//common_data//cad_number")
            adr = root.findall(".//readable_address")
            form = AddOKsForm(initial = {'cad_num': cn[0].text, 'adr_oks': adr[0].text})

    else:
        form = AddOKsForm()
        form2 = AddFiles()

    context = {
        'title': "Дабвление типа объекта",
        'form': form,
        'form2': form2,
        'user_is_login': request.user.is_authenticated
    }

    return render(request, 'list/add_tip.html', context=context)


def show_per(request, year_per=None):
    obj = Oks.objects.filter(per__year_per=year_per)

    if len(obj) == 0:
        raise Http404()

    try:
        year = Year.objects.get(pk=year_per)
    except ObjectDoesNotExist:
        raise Http404()

    context = {
        'title': "Перечень - " + str(year.name),
        'obj': obj,
    }
    return render(request, 'list/per.html', context=context)


class ObjListView(LoginRequiredMixin, DataMixin, ListView):
    model = Oks
    template_name = 'list/oks.html'
    context_object_name = 'obj'
    allow_empty = False
    login_url = '/admin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Объект - " + str(context['obj'].cad_num))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Oks.objects.get(pk=self.kwargs['oks_id'])


def show_tip(request, tip_id=None):
    try:
        obj = Oks.objects.filter(tip_oks=tip_id)
    except ObjectDoesNotExist:
        raise Http404()

    context = {
        'title': "Объекты - ",
        'obj': obj,
    }
    return render(request, 'list/tip.html', context=context)


@login_required(login_url='/admin/')
def add_obj(request):
    if request.method == 'POST':
        form = AddOKsForm2(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = AddOKsForm2()

    context = {
        'title': "Дабавление типа объекта",
        'form': form,
        'user_is_login': request.user.is_authenticated,
    }
    return render(request, 'list/add_obj.html', context=context)


@login_required(login_url='/admin/')
def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="list.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Перечень')

    row_num = 0
    num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'Кадастровый номер', 'Помещения', 'Адрес']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    data = request.GET.copy()
    if 'year_per' not in data:
        q = Year.objects.all().order_by('-id')
        if q.count() > 0:
            data['year_per'] = q.values('id')[0]['id']
    filtered_per = PerFilter(
        data,
        queryset=Per.objects.order_by('oks__adr_oks_sort')
    )
    filtered_per.helper = FormHelper()
    filtered_per.helper.form_show_labels = True
    filtered_per.helper.form_tag = False
    filtered_per.helper.layout = Layout(
        Field('year_per'),
        Field('oks__tip_oks'),
        Field('q'),
    )
    rows = filtered_per.qs
    for row in rows:
        row_num +=1
        num +=1
        ws.write(row_num, 0, num)
        if row.oks.tip_oks_id==2:
            ws.write(row_num, 2, row.oks.cad_num)
        else:
            ws.write(row_num, 1, row.oks.cad_num)
        ws.write(row_num, 3, row.oks.adr_oks)
        if row.oks.num_premises() > 0:
            prems = Premises.objects.filter(oks=row.oks.id)
            for prem in prems:
                ws.write(row_num, 2, prem.cad_num)
                row_num += 1
            row_num -= 1

    wb.save(response)
    return response


class ObjXML:
    def __init__(self, cad_name, tip, uu):
        self.cad_name = cad_name
        self.tip = tip
        self.uu = uu


@login_required(login_url='/admin/')
def export_xml(request):
    data = request.GET.copy()
    if 'year_per' not in data:
        q = Year.objects.all().order_by('-id')
        if q.count() > 0:
            data['year_per'] = q.values('id')[0]['id']
            year_name = q.values('id')[0]['name']
    else:
        q = Year.objects.get(pk=data['year_per'])
        year_name = q
    filtered_per = PerFilter(
        data,
        queryset=Per.objects.order_by('oks__adr_oks_sort')
    )
    filtered_per.helper = FormHelper()
    filtered_per.helper.form_show_labels = True
    filtered_per.helper.form_tag = False
    filtered_per.helper.layout = Layout(
        Field('year_per'),
        Field('oks__tip_oks'),
        Field('q'),
    )
    rows = filtered_per.qs
    obj = []

    for row in rows:
        obj_tec = ObjXML(row.oks.cad_num, row.oks.tip_oks_id, str(uuid.uuid4()))
        obj.append(obj_tec)
        if row.oks.num_premises() > 0:
            prems = Premises.objects.filter(oks=row.oks.id)
            for prem in prems:
                obj_tec = ObjXML(prem.cad_num, 2, str(uuid.uuid4()))
                obj.append(obj_tec)
    data_set = my_serialize(obj, year_name)
    response = HttpResponse(data_set, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="list.xml"'
    return response


@login_required(login_url='/admin/')
def export_word(request, **kwargs):
    obj = Oks.objects.get(id=kwargs['pk'])
    context = {'obj': obj}
    template_dir = os.path.join(settings.BASE_DIR, 'list', 'templates', 'list')
    docx = create_docx_document(template_dir, context)
    doc_io = io.BytesIO()  # create a file-like object
    docx.save(doc_io)  # save data to file-like object
    doc_io.seek(0)  # go to the beginning of the file-like object

    response = HttpResponse(doc_io.read())

    # Content-Disposition header makes a file downloadable
    response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return response


def create_docx_document(document_folder, document_context):

    doc = DocxTemplate(os.path.join(document_folder, 'doc_template.docx'))
    doc.render(document_context)
    return doc


def my_serialize(query_set, year):
    template_dir = os.path.join(settings.BASE_DIR, 'list', 'templates')
    yesterday = datetime.datetime.now()

    s_m = str(yesterday.month)
    if len(s_m) == 1:
        s_m = '0' + s_m

    s_d = str(yesterday.day)
    if len(s_d) == 1:
        s_d = '0' + s_d

    g_d = str(uuid.uuid4())
    xml_g = str(yesterday.year) + s_m + s_d + '_' + g_d
    Data_file = s_d + '.' + s_m + '.' + str(yesterday.year)

    xml = render_to_string(template_dir + '/list/xml_template.xml', {'query_set': query_set, 'xml_g': xml_g, 'Data_file':
        Data_file, 'year': year})
    return xml


class YearPerCreate(LoginRequiredMixin, DataMixin, CreateView):
    model = Year
    fields = ['name']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super(YearPerCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['oksobjects'] = PerFormSet(self.request.POST)
        else:
            data['oksobjects'] = PerFormSet()
        c_def = self.get_user_context(title="Годы")
        return dict(list(data.items()) + list(c_def.items()))

    def form_valid(self, form):
        context = self.get_context_data()
        oksobjects = context['oksobjects']
        with transaction.atomic():
            self.object = form.save()

            if oksobjects.is_valid():
                oksobjects.instance = self.object
                oksobjects.save()
        return super(YearPerCreate, self).form_valid(form)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'list/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('per')


def logout_user(request):
    logout(request)
    return redirect('login')