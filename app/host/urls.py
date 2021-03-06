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

from host import views
from asset.views import asset_repair_detail

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # --- host ---
    url(r'^host$', views.host, name="host"),
    url(r'^host/index$', views.host_index, name="host_index"),
    url(r'^host/repair$', views.host_repair, name="host_repair"),


    url(r'^host/repair/detail/(?P<pk>\d+)', views.host_repair_detail, name="host_repair_detail"),



    url(r'^host/(?P<pk>\d+)$', views.host_info, name="host_info"),
    url(r'^host/input', views.host_input, name="host_input"),
    url(r'^host/output', views.host_output, name="host_output"),

    # --- network ---

    # --- location ---
    url(r'^location/', views.location, name="location"),

    url(r'^demo1/', views.demo1),

]
