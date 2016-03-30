from django.contrib.auth import get_user_model
from django.views.generic import View
from rest_framework.authentication import TokenAuthentication

User = get_user_model()


class TokenAuthenticatedView(View, TokenAuthentication):
    def user_from_request(self):
        if 'authToken' in self.request.COOKIES:
            user, _ = self.authenticate_credentials(self.request.COOKIES['authToken'])
            return user
        else:
            return None

    def is_owner(self, restaurant):
        user = self.user_from_request()
        return user is not None and user == restaurant.owner
