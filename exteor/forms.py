from .models import Exteors
from django.forms import ModelForm, Form, TextInput, Select, DateTimeInput, Textarea, CharField, ChoiceField, HiddenInput, BooleanField, FileField

class UploadFileForm(Form):
    title = CharField(max_length=50)
    file = FileField()

class SchemaForm(ModelForm):
    error_css_class = 'error_text'

    class Meta:
        model = Exteors
        exclude = ['json_file', 'name']
        fields = ['schema', 'alias', 'common']

        choices = [(True, 'Да'), (False, 'Нет')]
        widgets = {
            'schema': TextInput(attrs={'class': 'form-control', 'placeholder': "Наименование схемы"}),
            'alias': TextInput(attrs={'class': 'form-control', 'placeholder': "Краткое наименование схемы"}),
            'common': Select(choices=choices, attrs={'class': 'form-control', 'placeholder': "Схема будет доступна для просмотра всем пользователям?"})
            # 'name': TextInput(attrs={'id': 'name_create', 'class': 'form-control', 'placeholder': "Имя"}),
        }

class ConstForm(Form):
    choices = [('basic', 'Базисное множество'), ('structure', 'Родовая структура'), ('function', 'Функция'),
               ('predicate', 'Предикат'), ('axiom', 'Аксиома'), ('term', 'Терм'), ('theorem', 'Теорема')]

    cstType = ChoiceField(help_text="Enter cstType", choices=choices, initial='basic', widget=Select(attrs={'class': 'form-control2', 'placeholder': "cstType"}))
    alias = CharField(help_text="Enter alias", widget=TextInput(attrs={'id': "alias_id", 'class': 'form-control3', 'placeholder': "alias"}))
    convention = CharField(required=False, help_text="Enter convention", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "convention"}))
    term_raw = CharField(help_text="Enter term_raw", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "term_raw"}))
    definition_formal = CharField(required=False, help_text="Enter definition_formal", widget=TextInput(attrs={'id': "inputSign", 'class': 'form-control2', 'placeholder': "definition_formal"}))
    definition_text_raw = CharField(required=False, help_text="Enter definition_text_raw", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "definition_text_raw"}))
    aliases = CharField(required=False, widget=HiddenInput(attrs={'id': "aliases"}))

# class SchemaForm(ModelForm):
#     def is_valid(self):
#         print('self.is_bound', self.is_bound)
#         print('self.errors', self.errors)
#         return self.is_bound and not self.errors
#
#     name = CharField(help_text="Enter name", widget=TextInput(attrs={'id': 'name_create', 'class': 'form-control', 'placeholder': "Имя"}))
#     schema = CharField(help_text="Enter schema", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "Схема"}))
#     type = CharField(help_text="Enter type", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "Тип"}))
#     cstType = CharField(help_text="Enter cstType", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "cstType"}))
#     alias = CharField(help_text="Enter alias", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "alias"}))
#     convention = CharField(help_text="Enter convention", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "convention"}))
#     term_raw = CharField(help_text="Enter term_raw", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "term_raw"}))
#     term_forms = CharField(help_text="Enter term_forms", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "term_forms"}))
#     term_type = CharField(help_text="Enter term_type", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "term_type"}))
#     definition_formal = CharField(help_text="Enter definition_formal", widget=TextInput(attrs={'id': "inputSign", 'class': 'form-control', 'placeholder': "definition_formal"}))
#     definition_text_raw = CharField(help_text="Enter definition_text_raw", widget=Textarea(attrs={'class': 'form-control', 'placeholder': "definition_text_raw"}))
#     definition_text_resolved = CharField(help_text="Enter definition_text_resolved", widget=TextInput(attrs={'class': 'form-control', 'placeholder': "Имя"}))
#
#     class Meta:
#         model = Exteors
#         exclude = ['name', 'schema', 'json_file']
#         # fields = ['name', 'schema', 'json_file']
#         #
#         # widgets = {
#         #     'name': TextInput(attrs={'id': 'name_create', 'class': 'form-control2', 'placeholder': "Имя"}),
#         #     'schema': TextInput(attrs={'class': 'form-control', 'placeholder': "Схема"}),
#         #     'json_file': Textarea(attrs={'id': "inputSign", 'class': 'form-control', 'placeholder': "JSON-file"}),
#         # }


# class ArticlesForm(ModelForm):
#     class Meta:
#         model = Articles
#         fields = ['schema', 'name', 'type', 'rs_definition', 'term', 'text_definition', 'result']
#
#         widgets = {
#             'schema': TextInput(attrs={'class': 'form-control', 'placeholder': "Схема"}),
#             'name': TextInput(attrs={'id': 'name_create', 'class': 'form-control2', 'placeholder': "Имя"}),
#             'type': TextInput(attrs={'id': 'type_create', 'class': 'form-control2', 'placeholder': "Тип"}),
#             'rs_definition': TextInput(attrs={'id': "inputSign", 'class': 'form-control', 'placeholder': "РС-определение"}),
#             'term': TextInput(attrs={'class': 'form-control', 'placeholder': "Термин"}),
#             'text_definition': Textarea(attrs={'class': 'form-control', 'placeholder': "Текстовое определение"}),
#             'result': TextInput(attrs={'class': 'form-control3', 'placeholder': "Результат расчета", 'readonly': 'readonly'}),
#         }