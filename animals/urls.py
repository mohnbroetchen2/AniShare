"""animals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/

Examples:

Function views:
  1. Add an import:  from my_app import views
  2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views:
  1. Add an import:  from other_app.views import Home
  2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf:
  1. Import the include() function: from django.urls import include, path
  2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

app_name = 'animals'
urlpatterns = [
#    path('', views.AnimalIndexView.as_view(), {'show':'current'}, name='animal-list'),
    path('', views.animal_list, name='animal-list'),
#    path('archive', views.AnimalIndexView.as_view(), {'show':'archive'}, name='archive'),
#    path('all', views.AnimalIndexView.as_view(), {'show':'all'}, name='all'),
    path('claim/<int:primary_key>', views.claim, name='claim'),
    path('send_email_animal', views.send_email_animal, name='send_email_animal'),
    path('send_email_organ', views.send_email_organ, name='send_email_organ'),
    path('<int:pk>', views.AnimalDetailView.as_view(), name='animal-detail'),
    path('feed', never_cache(views.LatestAnimalsFeed()), name='feed')
]
