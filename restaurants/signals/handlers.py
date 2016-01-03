from django.contrib.auth import get_user_model
from djoser.signals import user_registered
from django.dispatch import receiver
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class UserDisabler:
    @receiver(user_registered)
    def user_disabler(sender, user, **kwargs):
        logger.debug('Disabling registered user ' + user.username + ' until email is validated')
        user.is_active = False
        user.save()
