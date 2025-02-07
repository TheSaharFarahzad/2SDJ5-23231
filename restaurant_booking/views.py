from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken


class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()

        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response.data["access"] = access_token
        response.data["refresh"] = refresh_token

        response.data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }

        return response
