from django.contrib import admin
import uuid
import zipfile
from photo import settings
from datetime import datetime
from zipfile  import ZipFile
from django.core.files.base import ContentFile
from PIL import Image

from .models import Album, AlbumImages
from .forms  import AlbumForm

@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
	form = AlbumForm
	prepopulated_fields = {'slug': ('title',)}
	list_display        = ('title', 'thumb', 'created_date')
	list_filter         = ('created_date',)
	search_fields       = ('title',)

	def save_model(self, request, obj, form, change):
		if form.is_valid():
			album = form.save(commit=False)
			album.created_date  = datetime.now()
			album.modified_date = datetime.now()
			album.save()

			if form.cleaned_data['zip'] != None:
				zip = ZipFile(form.cleaned_data['zip'])
				for filename in sorted(zip.namelist()):
					data = zip.read(filename)
					contentfile = ContentFile(data)

					picture = AlbumImages()
					picture.album = album
					picture.alt   = filename
					filename    = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
					picture.picture.save(filename, contentfile)

					filepath = '{0}/albums/{1}'.format(settings.MEDIA_ROOT, filename)
					with picture.open(filename) as i:
						picture.width, picture.height = i.size
					picture.thumb.save('thumb-{0}'.format(filename), contentfile)
					picture.save()
				zip.close()

		super(AlbumModelAdmin, self).save_model(request, obj, form, change)
