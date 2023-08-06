from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from expressmoney import adapters


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
        bucket_name = settings.PROJECT
        super().__init__(bucket_name)
