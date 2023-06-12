from django.db import models

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
