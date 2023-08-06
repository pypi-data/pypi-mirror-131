from typing import Union

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from expressmoney import adapters


User = get_user_model()


class DjangoTasks(adapters.Tasks):

    def __init__(self, user: Union[int, User], queue: str = 'attempts-1', location: str = 'europe-west1',
                 project: str = 'expressmoney', in_seconds: int = None):
        if not isinstance(user, User):
            user = User.objects.get(pk=user)
        access_token = RefreshToken.for_user(user).access_token
        super().__init__(access_token, queue, location, project, in_seconds)
