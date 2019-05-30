
from django.urls import path
from . import views

urlpatterns = [
    path('', views.scraper, name="scraper.html"),
    path('results/', views.scraping_results, name="scraping_results.html")
]
