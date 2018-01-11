import os
import uuid
import zipfile
from photo    import settings
from PIL      import Image
from datetime import datetime
from zipfile  import ZipFile

from django.core.files.base import ContentFile

from django.conf           import settings
from django.http           import HttpRequest
from django.utils.crypto   import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth   import authenticate, login, logout
from django.contrib        import admin
from django.shortcuts      import render, redirect, HttpResponseRedirect, render_to_response
from django.views.generic  import  DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView

from .forms   import LoginForm, AlbumForm, AlbumUpdate
from .models  import Album, AlbumImages

def home(request):
	hash_phrase = get_random_string(length=24, allowed_chars='_0987654321&#$ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba')
	print(hash_phrase)
	return render(request, "slide.html", {})


def login_page(request):
	# print(request)
	message = None
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid:
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					message = "Te has logueado con éxito"
					return redirect('/gallery/')
				else:
					message = "Éste usuario esta inactivo"
					return render(request, 'login.html', {'message': message, 'form': form})
			else:
				message = "Nombre de usuario y/o contraseña incorrecto"
				return render(request, 'login.html', {'message': message, 'form': form})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'message': message, 'form': form})


def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')


@login_required
def nuevo_album(request):
	if request.method == "POST":
		# Access password/code
		hash_phrase = get_random_string(length=18, allowed_chars='_0987654321&#$ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba')

		form = AlbumForm(request.POST, request.FILES)

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

					img = AlbumImages()
					img.album = album
					img.alt   = filename
					filename  = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
					img.image.save(filename, contentfile)

					filepath = '{0}/albums/{1}'.format(settings.MEDIA_ROOT, filename)
					with Image.open(filepath) as i:
						img.width, img.height = i.size

					img.thumb.save('thumb-{0}'.format(filename), contentfile)
					img.save()
				zip.close()

			return redirect('/{0}'.format(request.POST['slug']))
		else:
			context = {
				'title': request.POST['title'],
				'description': request.POST['description'],
				'tags': request.POST['tags'],
				'slug': request.POST['slug'],
				'message': 'Error al procesar los datos.'
			}
			return render(request, 'album_nuevo.html', context)	
	else:
		form = AlbumForm()

	return render(request, 'album_nuevo.html', {})


@login_required(login_url='/login/')
def gallery(request):
	list = Album.objects.filter(is_visible=True).order_by('-created_date')

	paginator = Paginator(list, 10)

	#Test to generate solid hash password

	page = request.GET.get('page')
	try:
		albums = paginator.page(page)
	except PageNotAnInteger:
		albums = paginator.page(1) #Si página no es entero, mostrar la primara.
	except EmptyPage:
		albums = paginator.page(paginator.num_pages) #Si página esta fuera de rango, mostrar la ultima.

	return render(request, 'gallery.html', { 'albums': list })


# @login_required(login_url='/login/')
class AlbumDetail(DetailView):
	model = Album

	def get_context_data(self, **kwargs):
		context = super(AlbumDetail, self).get_context_data(**kwargs)

		context['images'] = AlbumImages.objects.filter(album=self.object.id)

		return context


class AlbumUpdate(UpdateView):
	template_name = 'app/album_update.html'
	form_class    = AlbumUpdate
	model         = Album

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.save()
		print(self.object)
		# if form.cleaned_data['zip'] != None:
		# 	zip = ZipFile(form.cleaned_data['zip'])
		# 	for filename in sorted(zip.namelist()):
		# 		data = zip.read(filename)
		# 		contentfile = ContentFile(data)

		# 		img = AlbumImages()
		# 		img.album = album
		# 		img.alt   = filename
		# 		filename  = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
		# 		img.image.save(filename, contentfile)

		# 		filepath = '{0}/albums/{1}'.format(settings.MEDIA_ROOT, filename)
		# 		with Image.open(filepath) as i:
		# 			img.width, img.height = i.size

		# 		img.thumb.save('thumb-{0}'.format(filename), contentfile)
		# 		img.save()
		# 	zip.close()

		return redirect('/{0}'.format(self.object.slug))


class AlbumDelete(DeleteView):
	model = Album
	success_url = '/gallery/'


def handler404(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)
