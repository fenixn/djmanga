from django.urls import path

from . import views
from manga.views import ScanView

app_name = 'manga'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('scan/', ScanView.as_view(), name='scan'),
    path('<slug:url_key>/', views.manga_view, name='manga-view'),
    path('<slug:url_key>/<int:chapter>/', views.chapter_view, name='chapter-view')
]