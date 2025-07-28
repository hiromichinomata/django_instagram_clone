from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    # Profile Section
    path('profile/edit', views.EditProfile, name="editprofile"),
]
