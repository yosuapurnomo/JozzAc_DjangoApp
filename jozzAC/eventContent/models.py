from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
def update_filename(instance, filename):
	ext 	= filename.split('.')[-1]
	filename 	= "%s.%s" % (instance.nama_Content, ext)
	return filename

def upload_location(instance, filename, **kwargs):
   path = update_filename(instance, filename)
   file_path = 'eventContent_media/{img}'.format(img=path)
   print('eventContent_media/{img}'.format(img=path))
   return file_path

class eventContentModel(models.Model):

   admin                     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
   nama_Content			     = models.CharField(max_length=20)
   image 			           = models.ImageField(upload_to=upload_location)
   keterangan_Content		  = models.TextField()
   tgl_upload                = models.DateField(auto_now_add=True)
   slug_Content			     = models.SlugField(blank=True, unique=True)

   class Meta:
      verbose_name='Event'

   def save(self):
      self.slug_Content	= slugify(f"{self.nama_Content}")
      super().save()

   def __str__(self):
      return f"{self.nama_Content}"


@receiver(post_delete, sender=eventContentModel)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

@receiver(pre_save, sender=eventContentModel)
def slug_save(sender, instance, **kwargs):
   if instance.slug_Content is not None:
      img = sender.objects.get(slug_Content=instance.slug_Content)
      img.delete(False)
      
