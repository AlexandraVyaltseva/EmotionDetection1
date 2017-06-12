from django.conf.urls import include, url
from django.contrib import admin
from face import views, forms
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.save_image_form, name='index'),
    # url(r'^view/(?P<pk>[a-z]{6})/$', forms.ImageView.as_view(), name='detail'),
    url(r'^face/(?P<id>[0-9]+)/$', views.detail, name='scores'),
    url(r'^face/', views.list, name='list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

