from django.urls import path
from flight_track import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('nth/', views.nth_route, name='nth_route'),
    path('create/', views.create_route, name='add_route'),
    path('longest/', views.longest_route, name='longest_route'),
    path('shortest/', views.shortest_route, name='shortest_route'),
    path('route/', views.route_list, name='route_list'),
]
