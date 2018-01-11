from django.db import models
import os
import uuid
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Album(models.Model):
	title         = models.CharField(max_length=100)
	description   = models.CharField(max_length=870)
	thumb         = models.FileField(upload_to='albums_thumb')
	tags          = models.CharField(max_length=250)
	is_visible    = models.BooleanField(default=True)
	created_date  = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now_add=True)
	slug          = models.SlugField(max_length=50, unique=True)

    #Python 3
	def __str__(self):
		return self.title

class AlbumImages(models.Model):
	image         = models.ImageField(upload_to='albums')
	thumb         = ProcessedImageField(upload_to='albums/thumbs', processors=[ResizeToFit(300)], format='JPEG', options={'quality': 85})
	alt           = models.CharField(max_length=255, default=uuid.uuid4)
	width         = models.IntegerField(default=900)
	height        = models.IntegerField(default=506)
	slug		  = models.CharField(max_length=70, default=uuid.uuid4, editable=False)
	album    	  = models.ForeignKey('album', on_delete=models.CASCADE,)
	created_date  = models.DateTimeField(auto_now_add=True)


class SlideImages(models.Model):
	image       = models.ImageField(upload_to='slides')
	is_active   = models.BooleanField(default=True)
	description = models.CharField(max_length=870)
	created_at  = models.DateTimeField(auto_now_add=True)



@receiver(models.signals.post_delete, sender=Album)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Delete thumb from filesystem when corresponding `Album` object is deleted.
    """
    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)


@receiver(models.signals.post_delete, sender=AlbumImages)
def auto_remove_file_on_delete(sender, instance, **kwargs):
    """
    Delete files from filesystem when corresponding `Album` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    if instance.thumb:
        if os.path.isfile(instance.thumb.path):
            os.remove(instance.thumb.path)
