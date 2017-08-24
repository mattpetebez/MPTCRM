"""SalesForce URL Configuration

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
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from SalesPeople import views as core_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/SalesPeople')),
    url(r'^ResetPassword/$', auth_views.password_reset, name='password_reset'),
    url(r'^ResetPassword/Done$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^ResetPassword/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)$', auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^ResetPassword/Complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^SalesPeople/', include('SalesPeople.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
]
