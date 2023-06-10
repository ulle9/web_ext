from django.shortcuts import render, redirect
from .models import Exteors
from .forms import SchemaForm, ConstForm, UploadFileForm, CreateUserForm
from django.views.generic import DetailView, UpdateView, DeleteView
import pyconcept
import json
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User

def exteor_home(request):
    schemas = Articles.objects.order_by('schema')
    return render(request, 'exteor/exteor-home.html', {'schemas': schemas})

#SCHEMAS
@login_required
def schemas_home(request):
    schemas = Exteors.objects.filter(name=request.user).order_by('-date_update', 'schema')
    return render(request, 'exteor/schemas-home.html', {'schemas': schemas})

def schemas_home_common(request):
    schemas = Exteors.objects.filter(common=True).order_by('-date_update', 'schema')
    return render(request, 'exteor/schemas-home-common.html', {'schemas': schemas})

@login_required
def schema_details(request, s_id):
    schema = Exteors.objects.get(pk=s_id)
    json_string = json.dumps(schema.json_file, ensure_ascii=False)
    parsed_json = json.loads(pyconcept.check_schema(json_string))
    data = {'schema': schema}
    status_dict = {'verified': 'ОК', 'incorrect': 'Ошибка'}
    for i, k in enumerate(schema.json_file['items']):

        schema.json_file['items'][i]['cstType'] = cst_type_dict[schema.json_file['items'][i]['cstType']]
        schema.json_file['items'][i]['parse']['status'] = status_dict[parsed_json['items'][i]['parse']['status']]
        schema.json_file['items'][i]['parse']['valueClass'] = parsed_json['items'][i]['parse']['valueClass']
        schema.json_file['items'][i]['parse']['typification'] = parsed_json['items'][i]['parse']['typification']

    # print(parsed_json)
    return render(request, 'exteor/schema-detail-view.html', data)

def schema_details_common(request, s_id):
    schema = Exteors.objects.get(pk=s_id)
    json_string = json.dumps(schema.json_file, ensure_ascii=False)
    parsed_json = json.loads(pyconcept.check_schema(json_string))
    data = {'schema': schema}
    status_dict = {'verified': 'ОК', 'incorrect': 'Ошибка'}
    for i, k in enumerate(schema.json_file['items']):

        schema.json_file['items'][i]['cstType'] = cst_type_dict[schema.json_file['items'][i]['cstType']]
        schema.json_file['items'][i]['parse']['status'] = status_dict[parsed_json['items'][i]['parse']['status']]
        schema.json_file['items'][i]['parse']['typification'] = parsed_json['items'][i]['parse']['typification']

    return render(request, 'exteor/schema-detail-view-common.html', data)

@login_required
def schema_create(request):
    error = ''
    if request.method == 'POST':
        form = SchemaForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            result_form = form.save(commit=False)
            result_form.json_file = {"type": "rsform", "title": "default", "alias": "default", "comment": "",
                                     "items": []}
            result_form.name = str(request.user)
            result_form.save()
            return redirect('exteor-schemas')
        else:
            if form.non_field_errors:
                error = "Такое сочетание 'Наименование - Пользователь' уже существует!"
            data = {'form': form, 'error': error}
            return render(request, 'exteor/schema-create.html', data)

    form = SchemaForm(initial={'name': str(request.user)})
    upload_form = UploadFileForm
    data = {'form': form, 'upload_form': upload_form, 'error': error}
    return render(request, 'exteor/schema-create.html', data)

def upload_file(request):
    error = ''
    if request.method == 'POST' and ('file' in request.FILES.keys()):
        myfile = request.FILES['file']
        try:
            for chunk in myfile.chunks():
                parsed_json = json.loads(chunk)
                form_dict = dict()
                form_dict['schema'] = parsed_json['title']
                form_dict['alias'] = parsed_json['alias']
                form_dict['name'] = str(request.user)
                break
        except:
            error = "Некорректные формат или структура файла!"
            form = SchemaForm(initial={'name': str(request.user)})
            data = {'form': form, 'error': error}
            return render(request, 'exteor/schema-create.html', data)

        form = SchemaForm(form_dict)
        if form.is_valid():
            form.save()
            result_form = form.save(commit=False)
            result_form.json_file = {"type": "rsform", "title": form_dict['schema'], "alias": form_dict['alias'], "comment": "", "items": parsed_json['items']}
            result_form.save()
        else:
            if form.non_field_errors:
                error = "Такое сочетание 'Наименование - Пользователь' уже существует!"
            form = SchemaForm(initial={'name': str(request.user)})
            data = {'form': form, 'error': error}
            return render(request, 'exteor/schema-create.html', data)

        return render(request, 'exteor/upload_success.html')
    else:
        return redirect('schema-create')

class SchemaUpdateView(UpdateView):
    model = Exteors
    template_name = 'exteor/schema-update.html'
    form_class = SchemaForm

class SchemaDeleteView(DeleteView):
    model = Exteors
    template_name = 'exteor/schema-delete.html'
    success_url = '/exteor/schemas'

def const_create(request, s_id):
    error = ''

    if request.method == 'POST':
        form = ConstForm(request.POST)
        if form.is_valid():
            entry = Exteors.objects.get(pk=s_id)
            uid = 0
            if entry.json_file['items']:
                for i in entry.json_file['items']:
                    if uid <= i['entityUID']:
                        uid_max = i['entityUID']
                        uid = uid_max
            else:
                uid_max = uid

            entry.json_file['items'].append({"entityUID": "", "type": "constituenta", "cstType": "", "alias": "", "convention": "",
                         "term": {"raw": "", "resolved": "", "forms": []},
                         "definition": {"formal": "", "text": {"raw": "", "resolved": ""}},
                         "parse": {"status": "", "valueClass": "", "typification": "", "syntaxTree": ""}})
            idx = len(entry.json_file['items']) - 1

            entry.json_file['items'][idx]['entityUID'] = uid_max + 1
            entry.json_file['items'][idx]['cstType'] = form.cleaned_data['cstType']
            entry.json_file['items'][idx]['alias'] = form.cleaned_data['alias']
            entry.json_file['items'][idx]['convention'] = form.cleaned_data['convention']
            entry.json_file['items'][idx]['term']['raw'] = form.cleaned_data['term_raw']
            entry.json_file['items'][idx]['definition']['formal'] = form.cleaned_data['definition_formal']
            entry.json_file['items'][idx]['definition']['text']['raw'] = form.cleaned_data['definition_text_raw']
            entry.save()

            return redirect('schema-detail', s_id)
        else:
            error = "Форма заполнена некорректно!"
    else:
        entry = Exteors.objects.get(pk=s_id)
        items = entry.json_file['items']
        aliases = []
        for i in items:
            aliases.append(i['alias'])
        aliases = ' '.join(aliases)
        form = ConstForm(initial={'aliases': aliases})
        data = {'form': form, 'error': error, 'schema': s_id}
        return render(request, 'exteor/const-create.html', data)

def const_update(request, s_id, c_id):
    error = ''
    if request.method == 'POST':
        form = ConstForm(request.POST)
        if form.is_valid():
            entry = Exteors.objects.get(pk=s_id)
            uid = 0
            for i in entry.json_file['items']:
                if uid < i['entityUID']:
                    uid_max = i['entityUID']
                    uid = uid_max
            for id, val in enumerate(entry.json_file['items']):
                if val['entityUID'] == c_id:
                    idx = id
                    break

            entry.json_file['items'][idx]['entityUID'] = uid_max + 1
            entry.json_file['items'][idx]['cstType'] = form.cleaned_data['cstType']
            entry.json_file['items'][idx]['alias'] = form.cleaned_data['alias']
            entry.json_file['items'][idx]['convention'] = form.cleaned_data['convention']
            entry.json_file['items'][idx]['term']['raw'] = form.cleaned_data['term_raw']
            entry.json_file['items'][idx]['definition']['formal'] = form.cleaned_data['definition_formal']
            entry.json_file['items'][idx]['definition']['text']['raw'] = form.cleaned_data['definition_text_raw']
            entry.save()

            return redirect('schema-detail', s_id)
        else:
            error = "Форма заполнена некорректно!"

    else:
        entry = Exteors.objects.get(pk=s_id)

        items = entry.json_file['items']
        aliases = []
        for i in items:
            if i['entityUID'] != c_id:
                aliases.append(i['alias'])
        aliases = ' '.join(aliases)

        for id, val in enumerate(entry.json_file['items']):
            if val['entityUID'] == c_id:
                idx = id
                break
        json_init = entry.json_file['items'][idx]
        form = ConstForm(initial={'cstType': json_init['cstType'],
                                  'alias': json_init['alias'],
                                  'convention': json_init['convention'],
                                  'term_raw': json_init['term']['raw'],
                                  'definition_formal': json_init['definition']['formal'],
                                  'definition_text_raw': json_init['definition']['text']['raw'],
                                  'aliases': aliases})

        data = {'form': form, 'error': error, 'schema': s_id, 'const': c_id}
        return render(request, 'exteor/const-update.html', data)

def const_delete(request, s_id, c_id):
    if request.method == 'POST':
        entry = Exteors.objects.get(pk=s_id)
        for id, val in enumerate(entry.json_file['items']):
            if val['entityUID'] == c_id:
                idx = id
                break
        entry.json_file['items'].pop(idx)
        entry.save()
        return redirect('schema-detail', s_id)

    data = {'schema': s_id, 'const': c_id}
    return render(request, 'exteor/const-delete.html', data)

def const_view(request, s_id, c_id):
    entry = Exteors.objects.get(pk=s_id)
    items = entry.json_file['items']
    aliases = []
    for i in items:
        if i['entityUID'] != c_id:
            aliases.append(i['alias'])

    aliases = ' '.join(aliases)

    for id, val in enumerate(entry.json_file['items']):
        if val['entityUID'] == c_id:
            idx = id
            break

    json_init = entry.json_file['items'][idx]
    form = ConstForm(initial={'cstType': json_init['cstType'],
                            'alias': json_init['alias'],
                            'convention': json_init['convention'],
                            'term_raw': json_init['term']['raw'],
                            'definition_formal': json_init['definition']['formal'],
                            'definition_text_raw': json_init['definition']['text']['raw'],
                            'aliases': aliases})

    data = {'form': form, 'schema': s_id, 'const': c_id}
    return render(request, 'exteor/const-view.html', data)

class SignUpView(generic.CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("login")
    template_name = "exteor/signup.html"
    model = User

cst_type_dict = {'basic': 'Базисное множество', 'structure': 'Родовая структура', 'function': 'Функция', 'predicate': 'Предикат', 'axiom': 'Аксиома', 'term': 'Терм', 'theorem': 'Теорема'}
