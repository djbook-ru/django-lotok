
import hashlib
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import TreeForeignKey, MPTTModel

from hranilishe.filesystem import *


class Category(MPTTModel):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                                        related_name='children', db_index=True)

    class Meta:
        verbose_name = u'category'
        verbose_name_plural = u'category'
        ordering = ('name', )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_hidden = models.BooleanField(_(u'Do not show this product'), default=False)
    registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(u'machine')
        verbose_name_plural = _(u'machines')
        ordering = ('name', )

    def __unicode__(self):
        return u'{}: {}'.format(self.name, self.dimension)


class Property(models.Model):
    product = models.ForeignKey(Product)
    key = models.CharField(verbose_name=_(u'title'), max_length=64)
    value = models.CharField(verbose_name=_(u'value'), max_length=128)

    class Meta:
        verbose_name = _(u'Property')
        verbose_name_plural = _(u'Properties')
        ordering = ('key',)

    def __unicode__(self):
        return self.key


class Media(models.Model):
    filename = models.CharField(max_length=255, blank=True, null=True)
    resource = models.FileField(_(u'model'), max_length=256,
                                upload_to=upload_by_hash,
                                storage=HashedFileSystemStorage())
    size = models.PositiveIntegerField(default=0, help_text=_(u'The size of the uploaded detail.'))
    is_compressed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    registered = models.DateTimeField(auto_now_add=True)

    # служебное поле, используется для организации хранения файлов,
    # см. функцию upload_by_hash выше
    md5sum = models.CharField(max_length=36)

    def save(self, *args, **kwargs):
        u"""Вычисляет MD5 от содержимого файла и записывает его в поле модели.
        При сохранении функция upload_by_hash берёт вычисленный хэш из модели и
        записывает на файловую систему с помощью HashedFileSystemStorage.
        """
        if not self.pk:  # сохранение нового объекта
            md5 = hashlib.md5()
            for chunk in self.resource.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
            self.size = self.resource.file.size
        super(Media, self).save(*args, **kwargs)
