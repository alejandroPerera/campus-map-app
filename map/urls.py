from django.urls import path

from . import views

app_name = 'map'
urlpatterns = [
    path('', views.MapView.as_view(), name='map'),
    path('search/', views.get_class_search_results, name='search'),  # For handling search query's
    path('addClass/', views.add_class, name='addClass'),
    path('removeClass/', views.remove_class, name='removeClass'),
    path('makeEvent/', views.user_created_event, name='makeEvent'),
    path('attendEvent/',views.attend_event, name = "attendEvent"),
    path('cancelEvent/', views.cancel_event, name = 'cancelEvent'),
    path('removeEvent/', views.remove_event_from_list, name = 'removeEvent'),
]
