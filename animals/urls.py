"""animals URL Configuration

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

from django.urls import path
from . import views

app_name = 'animals'
urlpatterns = [
    path('', views.AnimalIndexView.as_view(), {'show':'current'}, name='animal-list'),
    path('index', views.AnimalIndexView.as_view(), {'show':'current'}, name='index'),
    path('archive', views.AnimalIndexView.as_view(), {'show':'archive'}, name='archive'),
    path('all', views.AnimalIndexView.as_view(), {'show':'all'}, name='all'),
    path('claim/<int:pk>', views.claim, name='claim'),
    path('send_email', views.send_email, name='send_email'),
    path('<int:pk>', views.AnimalDetailView.as_view(), name='animal-detail'),
    path('feed', views.LatestAnimalsFeed(), name='feed')

    #    path('add', views.AnimalCreateView.as_view(), name='animal-add'),
    #    path('<int:pk>/edit', views.AnimalUpdateView.as_view(), name='animal-update'),
    #    path('<int:pk>/delete', views.AnimalDeleteView.as_view(), name='animal-delete'),
]
