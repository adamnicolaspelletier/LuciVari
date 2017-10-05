"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import include
from lucivari import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse


# Create a new class that redirects the user to the index page, 
#if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^lucivari/', include('lucivari.urls')),
    # above maps any URLs starting 
    # with rango/ to be handled by
    # the rango application
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', 
    MyRegistrationView.as_view(), 
        name='registration_register'),
#==============================================================================
#     url(r'^accounts/password/change/$', password_change.as_view(), name='password_change'),
#     url(r'^accounts/password/change/done/$', password_change_done.as_view(), name='password_change_done'),
#==============================================================================
    url(r'^accounts/', include('registration.backends.simple.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
