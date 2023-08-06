from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from expressmoney import adapters
from expressmoney.adapters import Request

User = get_user_model()


class DjangoTasks(adapters.Tasks):

    def __init__(self, user: Union[int, User], queue: str = 'attempts-1', location: str = 'europe-west1',
                 in_seconds: int = None):
        if not isinstance(user, User):
            user = User.objects.get(pk=user)
        access_token = RefreshToken.for_user(user).access_token
        project = settings.PROJECT
        super().__init__(access_token, queue, location, project, in_seconds)


class DjangoPubSub(adapters.PubSub):

    def __init__(self, topic_id: str, user: Union[None, int, User] = None):
        if user:
            if not isinstance(user, User):
                user = User.objects.get(pk=user)
            access_token = RefreshToken.for_user(user).access_token
        else:
            access_token = None
        project = settings.PROJECT
        super().__init__(topic_id, access_token, project)


class DjangoStorage(adapters.Storage):
    def __init__(self):
        bucket_name = f'{settings.PROJECT}.appspot.com'
        super().__init__(bucket_name)


class DjangoRequest(Request):

    def __init__(self, service: str = None, path: str = '/', user: Union[int, User] = None):
        user = user if isinstance(user, User) else User.objects.get(pk=user)
        access_token = RefreshToken.for_user(user).access_token if user else None
        project = settings.PROJECT
        super().__init__(service, path, access_token, project)

    def _get_authorization(self) -> dict:
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token
        authorization = super()._get_authorization()
        open_id_connect_token = id_token.fetch_id_token(Request(), settings.IAP_CLIENT_ID)
        iap_token = {'Authorization': f'Bearer {open_id_connect_token}'}
        authorization.update(iap_token)
        return authorization
