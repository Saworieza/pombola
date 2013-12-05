from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from sorl.thumbnail import ImageField


class SlideQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class SlideManager(models.Manager):
    def get_query_set(self):
        return SlideQuerySet(self.model, using=self._db)

    def random_slide(self):
        return self.all().active().order_by('?')[0]


class Slide(models.Model):
    sort_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    # link to other objects using the ContentType system
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = SlideManager()

    def __unicode__(self):
        return u"Slide of '{}'".format( self.content_object )

    class Meta(object):
        ordering = ( 'sort_order', 'id' )


class ImageContent(models.Model):
    """
    Model for image content for the spinner.
    """
    image = ImageField(upload_to="spinner_images")
    caption = models.CharField(max_length=300)
    url = models.URLField()

    def __unicode__(self):
        return self.caption

    class Meta(object):
        verbose_name_plural = 'images'


class QuoteContent(models.Model):
    """
    Model for image content for the spinner.
    """
    quote = models.TextField()
    attribution = models.CharField(max_length=300)
    url = models.URLField()

    def __unicode__(self):
        return self.quote

    class Meta(object):
        verbose_name_plural = 'quotes'

