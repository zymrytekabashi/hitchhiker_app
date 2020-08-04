from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('trips/new', views.new_trip),
    path('trips/create', views.create_trip),
    path('trips/<int:id>', views.view_trip),
    path('trips/reserve/<int:id>', views.reserve_seat),
    path('trips/add_comment/<int:trip_id>', views.add_comment),
    path('trips/<int:id>/delete', views.destroy),
    path('trips/edit/<int:id>', views.edit_trip),
    path('trips/update/<int:id>', views.update),
    path('log_out', views.log_out),
]