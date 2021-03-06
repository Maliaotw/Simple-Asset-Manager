"""AutoCmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from asset.views import acc_login, acc_logout
from api import views

urlpatterns = [

                  url(r'^login/', acc_login, name="login"),
                  url(r'^logout/', acc_logout, name="logout"),

                  url(r'^admin/', admin.site.urls),
                  # url(r'^host/', include('host.urls')),
                  url(r'^', include('host.urls')),
                  url(r'^api/', include('api.urls')),
                  url(r'^', include('asset.urls')),
                  url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),

              ] + static(settings.DEMO_URL, document_root=settings.DEMO_ROOT)
