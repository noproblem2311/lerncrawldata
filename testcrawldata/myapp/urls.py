from django.urls import path
from myapp import views
urlpatterns = [
    
    # path('ielts1', views.index, name='index'),
    path('orange', views.testCrawlCsv, name='crawlorangedata'),
    path('', views.timtruyen, name='test'),
]