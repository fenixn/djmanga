from django.urls import path

from . import views
from book.views import ScanView

app_name = 'book'
urlpatterns = [
    path('', views.IndexView.as_view(), name='book-index'),
    path('scan/', ScanView.as_view(), name='scan'),
    path('<slug:url_key>/', views.book_view, name='book-view'),
    path('<slug:url_key>/<int:chapter>/', views.chapter_view, name='chapter-view')
]