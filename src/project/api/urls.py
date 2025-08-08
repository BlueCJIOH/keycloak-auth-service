from django.urls import path
from .views import get_healthz

urlpatterns = [
    path("healthz/", get_healthz, name="healthz"),
]
