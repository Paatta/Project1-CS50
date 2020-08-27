from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.entry, name="entry"),
    path("Create",views.create,name="create"),
    path("wiki/<str:entry>/Edit",views.editpage,name="editpage"),
    path("Random",views.randompage,name="random")
]
