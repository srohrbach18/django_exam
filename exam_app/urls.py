from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path("groups/create", views.create_group),
    path("groups/<int:group_id>", views.show_one),
    path("join/<int:group_id>", views.join),
    path("leave/<int:group_id>", views.leave),
    path('delete/<int:group_id>', views.delete_group)
]