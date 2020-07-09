from django.urls import path

from . import views

app_name = 'tags'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:tag>/', views.tag_view, name='tag-view')
]