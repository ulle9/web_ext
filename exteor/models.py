from django.db import models

# class Articles(models.Model):
#     schema = models.CharField('Название', max_length=100)
#     name = models.CharField('Имя', max_length=100)
#     type = models.CharField('Тип', max_length=100)
#     rs_definition = models.CharField('РС-определение', max_length=300)
#     term = models.CharField('Термин', max_length=500)
#     text_definition = models.TextField('Текстовое определение')
#     result = models.CharField('Результат', max_length=500, default='Расчет не производился')
#
#
#     def __str__(self):
#         return self.schema
#
#     def get_absolute_url(self):
#         return '/exteor/{}'.format(self.id)
#
#     class Meta:
#         verbose_name = 'Запись'
#         verbose_name_plural = 'Записи'

class Exteors(models.Model):
    name = models.CharField('Пользователь', max_length=50)
    common = models.BooleanField('Общая', default=False)
    schema = models.CharField('Название', max_length=200)
    alias = models.CharField('Краткое название', blank=True, max_length=50)
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Дата изменения', auto_now=True)
    json_file = models.JSONField('Схема', null=True)

    def __str__(self):
        return self.name + "/" + self.schema

    def get_absolute_url(self):
        return '/exteor/schemas/{}'.format(self.id)


    class Meta:
        verbose_name = 'Схема'
        verbose_name_plural = 'Схемы'
        unique_together = ('name', 'schema')
