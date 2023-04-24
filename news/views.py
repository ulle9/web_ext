from django.shortcuts import render, redirect
from .models import Articles, Exteors
from .forms import ArticlesForm, SchemaForm, ConstForm
from django.views.generic import DetailView, UpdateView, DeleteView
import pyconcept
import json
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
# from django.forms.models import model_to_dict

def news_home(request):
    schemas = Articles.objects.order_by('schema')
    return render(request, 'news/news-home.html', {'schemas': schemas})

class NewsDetailView(DetailView):
    model = Articles
    context_object_name = 'article'
    template_name = 'news/detail-view.html'

class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = 'news/news-delete.html'
    success_url = '/news'

def create(request):
    error = ''
    if request.method == 'POST':
        #print('request.body', request.body)
        form = ArticlesForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.result = str3_module.str3_func(new_form.schema, new_form.name, new_form.type)
            new_form.save()
            id = list(Articles.objects.values('id'))[-1]['id']
            data = {'form': new_form, 'error': error, 'result': new_form.result, 'id': id}
            #print("last_schema[-1]", last_schema[-1]['id'])
            return render(request, 'news/calculated.html', data)
        else:
            error = "Форма заполнена некорректно!"

    form = ArticlesForm()
    data = {'form': form, 'error': error}
    return render(request, 'news/create.html', data)

def calculated(request):
    error = ''

    if request.method == 'POST':
        print('SECOND')
        form = ArticlesForm(request.POST)
        for field in form:
             print("Field Error:", field.name, field.errors)

        if form.is_valid():
            print('THIRD')
            new_form = form.save(commit=False)
            new_form.result = (str3_module.str3_func(new_form.schema, new_form.name, new_form.type))
            new_form.save()
            return redirect('news_home')

    form = ArticlesForm()
    data = {'form': form, 'error': error}
    return render(request, 'news/create.html', data)

#SCHEMAS
@login_required
def schemas_home(request):
    schemas = Exteors.objects.filter(name=request.user).order_by('-date_update', 'schema')
    print('schemas_home', request.user)
    return render(request, 'news/schemas-home.html', {'schemas': schemas})

def schemas_home_common(request):
    schemas = Exteors.objects.filter(common=True).order_by('-date_update', 'schema')
    print('schemas_home_common', request.user)
    return render(request, 'news/schemas-home-common.html', {'schemas': schemas})

@login_required
def schema_details(request, s_id):
    schema = Exteors.objects.get(pk=s_id)
    json_string = json.dumps(schema.json_file, ensure_ascii=False)
    parsed_json = json.loads(pyconcept.check_schema(json_string))
    # print(c_json)
    # print(type(schema.json_file), schema.json_file)
    # schema.json_file = parsed_json
    data = {'schema': schema}
    for i, k in enumerate(schema.json_file['items']):
        # print(schema.json_file['items'][i]['parse'])
        # cst_type_dict
        schema.json_file['items'][i]['cstType'] = cst_type_dict[schema.json_file['items'][i]['cstType']]
        schema.json_file['items'][i]['parse']['status'] = parsed_json['items'][i]['parse']['status']
        schema.json_file['items'][i]['parse']['valueClass'] = parsed_json['items'][i]['parse']['valueClass']
        schema.json_file['items'][i]['parse']['typification'] = parsed_json['items'][i]['parse']['typification']
        # print(schema.json_file['items'][i]['parse'])
    # print(type(schema.json_file))
    # print(type(pyconcept.check_schema(json_string)))
    # print(type(parsed_json))
    # items = schema.json_file
    # print(type(items))

    # for idx, i in enumerate(schema.json_file.items.items()):
    #     print(idx, i)
    print(parsed_json)
    return render(request, 'news/schema-detail-view.html', data)

def schema_details_common(request, s_id):
    schema = Exteors.objects.get(pk=s_id)
    json_string = json.dumps(schema.json_file, ensure_ascii=False)
    parsed_json = json.loads(pyconcept.check_schema(json_string))
    data = {'schema': schema}

    for i, k in enumerate(schema.json_file['items']):
        # print(schema.json_file['items'][i]['parse'])
        # cst_type_dict
        schema.json_file['items'][i]['cstType'] = cst_type_dict[schema.json_file['items'][i]['cstType']]
        schema.json_file['items'][i]['parse']['status'] = parsed_json['items'][i]['parse']['status']
        schema.json_file['items'][i]['parse']['typification'] = parsed_json['items'][i]['parse']['typification']

    return render(request, 'news/schema-detail-view-common.html', data)

@login_required
def schema_create(request):
    error = ''
    if request.method == 'POST':
        form = SchemaForm(request.POST)
        if form.is_valid():
            form.save()
            result_form = form.save(commit=False)
            result_form.json_file = {"type": "rsform_0", "title": "default", "alias": "default", "comment": "",
                                     "items": []}
            result_form.name = str(request.user)
            print(result_form.name, result_form.common)
            result_form.save()
            return redirect('exteor-schemas')
        else:
            if form.non_field_errors:
                error = "Такое сочетание 'Наименование - Пользователь' уже существует!"
            data = {'form': form, 'error': error}
            return render(request, 'news/schema-create.html', data)

    form = SchemaForm()
    data = {'form': form, 'error': error}
    return render(request, 'news/schema-create.html', data)

class SchemaUpdateView(UpdateView):
    model = Exteors
    template_name = 'news/schema-update.html'
    form_class = SchemaForm

class SchemaDeleteView(DeleteView):
    model = Exteors
    template_name = 'news/schema-delete.html'
    success_url = '/news/schemas'

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

            # print(entry.json_file)
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
        return render(request, 'news/const-create.html', data)

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
            # print(id, val['entityUID'], c_id)
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
        return render(request, 'news/const-update.html', data)

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
    return render(request, 'news/const-delete.html', data)

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
    return render(request, 'news/const-view.html', data)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "news/signup.html"

cst_type_dict = {'basic': 'Базисное множество', 'structure': 'Родовая структура', 'function': 'Функция', 'predicate': 'Предикат', 'axiom': 'Аксиома', 'term': 'Терм', 'theorem': 'Теорема'}

test_json = '''{"type": "rsform", "title": "default","alias": "default","comment": "", "items": [{"entityUID": 1023383816, "type": "constituenta", "cstType": "basic","alias": "X1", "convention": "", "term": {"raw": "", "resolved": "",  "forms": []}, "definition": {"formal": "", "text": { "raw": "", "resolved": ""}}},{"entityUID": 1877659352, "type": "constituenta", "cstType": "basic", "alias": "X2", "convention": "", "term": {"raw": "", "resolved": "", "forms": []}, "definition": {"formal": "", "text": {"raw": "", "resolved": ""}}},{"entityUID": 1115937389, "type": "constituenta", "cstType": "structure", "alias": "S1", "convention": "", "term": {"raw": "", "resolved": "", "forms": []}, "definition": {"formal": "ℬ(X1×X1)", "text": { "raw": "", "resolved": ""}}},{"entityUID": 94433573, "type": "constituenta", "cstType": "structure", "alias": "S2", "convention": "", "term": { "raw": "", "resolved": "", "forms": []}, "definition": { "formal": "ℬ(X1×X2)", "text": {"raw": "", "resolved": ""}}}]}'''