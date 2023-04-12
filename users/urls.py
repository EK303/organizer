from django.urls import path, include
from .views import RegisterUserView, ActivateView, LoginView, PasswordChangeView


urlpatterns = [
    path("registration/", RegisterUserView.as_view(), name="register"),
    path("registration/activate/", ActivateView.as_view(), name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("change_password/", PasswordChangeView.as_view(), name="change_password"),
    path("api/password_reset", include('django_rest_passwordreset.urls', namespace='password_reset')),
]