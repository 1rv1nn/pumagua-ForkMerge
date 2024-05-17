from django.contrib import admin
from django.urls import path

import pumaguaAPP.views as views

app_name = "pumaguaAPP"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='Home'),
    path('reportes/', views.cargaReportes, name='cargaReportes'),
    path('nombre1/', views.nombre1, name='nombre1'),
    path('nombre2/', views.nombre2, name='nombre2')
]
