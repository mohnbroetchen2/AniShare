"""anishare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from animals import urls
import animals

urlpatterns = [
#    path('', animals.views.AnimalIndexView.as_view(), name='root'),
    path('', animals.views.animal_list, name='animal-list'),
    path('animals/', include('animals.urls', namespace='animals-index')),
    path('organs/', animals.views.organ_list, name='organs'),
    path('organs/claim/<int:primary_key>', animals.views.claim_organ, name='claim_organ'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('macros/', animals.views.macros, name='macro'),
    path('changehistory/', animals.views.change_history, name='change'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
