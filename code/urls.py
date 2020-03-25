"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include
from myapp.home import views as homeViews
from myapp.item import views as itemViews


# http://localhost:8000/products/?skin_type=oily&category=skincare&page=3&include_ingredient=waterfall
# http://localhost:8000/product/1000/?skin_type=oily
urlpatterns = [
    path('admin/', admin.site.urls),
    #path(r'', homeView.index),

    path('init/DB', itemViews.initDB),   #Seed Data
    path('all/DB', itemViews.printAll),  #Print All Data
    
    re_path(r'products/$', itemViews.getItemsListView), # Items List
    path('product/<int:pk>/', itemViews.getItemDetailView),  # Item Detail Info

]