from django.urls import path

from . import views

app_name = 'person'
urlpatterns = [
    path('', views.IndexView.as_view(), name='person-index'),
    path('<slug:slug>/', views.person_view, name='person-view')
]