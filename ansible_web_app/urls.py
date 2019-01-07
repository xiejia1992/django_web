"""ansible web URL Configuration
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
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from ansible_web_app import views


urlpatterns = [
    url(r'^$', views.ansible_index),
    url(r'^api/groups/$', views.group_list),
    url(r'^api/groups/(?P<id>(\d+))/$', views.group_detail),
    url(r'^api/ips/$', views.ip_list),
    url(r'^api/ips/(?P<id>(\d+))/$', views.ip_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
