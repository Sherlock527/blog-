from django.conf.urls import url
from .views import reg, show, login, test

urlpatterns = [
    url(r'^reg/?$', reg),
    url(r'^show/?$', show),
    url(r'^login/?$', login),
    url(r'^test/?$', test)
]