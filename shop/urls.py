from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.shop, name="shop"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("product/<int:myid>", views.product, name="product"),
    path("checkout/", views.checkout, name="checkout"),
    path("tracker/", views.tracker, name="tracker"),
    path("RequestHandler/", views.RequestHandler, name="RequestHandler"),
    path("search/",views.search,name="search")
]
