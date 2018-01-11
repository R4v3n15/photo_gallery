"""photo URL Configuration

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic.base import RedirectView
from django.conf.urls.static   import static
from django.conf    import settings
from django.contrib import admin
from django.urls    import path, include
from app            import views

admin.autodiscover()

urlpatterns = [
	path('',            views.home,        name='home'),
	path('newalbum/',   views.nuevo_album,  name='newalbum'),
    path('login/',      views.login_page,  name='login'),
    path('logout/',     views.logout_user, name='logout'),
    path('gallery/',    views.gallery,     name='gallery'),
    path('<slug>',      views.AlbumDetail.as_view(), name='album'),
    path('update/<slug>', views.AlbumUpdate.as_view(), name='update'),
    path('delete/<slug>',   views.AlbumDelete.as_view(), name='delete'),
    path('admin/',        admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)