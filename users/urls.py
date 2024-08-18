from django.urls import path, re_path

from users import views as users_view

urlpatterns = [
    path("login", users_view.login_page, name="login"),
    path("logout", users_view.logout_page, name="logout"),
    path("home-page", users_view.home_page, name="home-page"),
    re_path(r"^(?!media.*).*", users_view.default, name="default"),
]
