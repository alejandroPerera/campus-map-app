from django.urls import path

from . import views

app_name = 'map'
urlpatterns = [
    path('', views.MapView.as_view(), name='map'),
    path('search/', views.get_search_results, name='search'), # For handling search query's
    path('searchForClassModel/', views.get_class_model_results, name='searchForClassModel'),
    path('addClass/', views.add_class, name='addClass')
]
