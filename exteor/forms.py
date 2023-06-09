from .models import Exteors
from django.forms import ModelForm, Form, TextInput, Select, DateTimeInput, Textarea, CharField, ChoiceField, HiddenInput, BooleanField, FileField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UploadFileForm(Form):
    title = CharField(max_length=50)
    file = FileField()

class SchemaForm(ModelForm):
    error_css_class = 'error_text'

    class Meta:
        model = Exteors
        exclude = ['json_file']
        fields = ['schema', 'alias', 'common', 'name']
        choices = [(True, 'Да'), (False, 'Нет')]
        widgets = {
            'schema': TextInput(attrs={'class': 'form-control', 'placeholder': "Наименование схемы"}),
            'alias': TextInput(attrs={'class': 'form-control', 'placeholder': "Краткое наименование схемы"}),
            'common': Select(choices=choices, attrs={'class': 'form-control', 'placeholder': "Схема будет доступна для просмотра всем пользователям?"}),
            'name': TextInput(attrs={'id': 'name_create', 'class': 'form-control', 'placeholder': "Имя"}),
        }

class ConstForm(Form):
    choices = [('basic', 'Базисное множество'), ('structure', 'Родовая структура'), ('function', 'Функция'),
               ('predicate', 'Предикат'), ('axiom', 'Аксиома'), ('term', 'Терм'), ('theorem', 'Теорема')]

    cstType = ChoiceField(help_text="Enter cstType", choices=choices, initial='basic', widget=Select(attrs={'class': 'form-control4', 'placeholder': "Конституента"}))
    alias = CharField(help_text="Enter alias", widget=TextInput(attrs={'id': "alias_id", 'class': 'form-control4', 'placeholder': "Идентификатор"}))
    convention = CharField(required=False, help_text="Enter convention", widget=TextInput(attrs={'class': 'form-control4', 'placeholder': "Комментарий"}))
    term_raw = CharField(help_text="Enter term_raw", widget=TextInput(attrs={'class': 'form-control4', 'placeholder': "Термин"}))
    definition_formal = CharField(required=False, help_text="Enter definition_formal", widget=TextInput(attrs={'id': "inputSign", 'class': 'form-control4', 'placeholder': "РС-определение"}))
    definition_text_raw = CharField(required=False, help_text="Enter definition_text_raw", widget=TextInput(attrs={'class': 'form-control4', 'placeholder': "Текстовое определение"}))
    aliases = CharField(required=False, widget=HiddenInput(attrs={'id': "aliases"}))

class CreateUserForm(UserCreationForm):
   class Meta(UserCreationForm.Meta):
       model = User
       fields = ['username', 'email']
