from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _


class CommonAccess(models.Model):
    user_agent = models.CharField(
        verbose+name=_('User Agent'),
        max_length=255,
        db_index=True,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address'),
        null=True,
        db_index=True,
    )

    username = models.CharField(
        verbose_name=_('Username'),
        max_length=255,
        null=True,
        db_index=True,
    )

    # Once a user logs in from an ip, that combination is trusted and not
    # locked out in case of a distributed attack
    trusted = models.BooleanField(
        default=False,
        db_index=True,
    )

    http_accept = models.CharField(
        verbose_name=_('HTTP Accept'),
        max_length=1025,
    )

    path_info = models.CharField(
        verbose_name=_('Path'),
        max_length=255,
    )

    attempt_time = models.DateTimeField(
        verbose_name=_('Attempt Time'),
        auto_now_add=True,
    )

    class Meta(object):
        app_label = 'axes'
        abstract = True
        ordering = ['-attempt_time']


class AccessAttempt(CommonAccess):
    get_data = models.TextField(
        verbose_name=_('GET Data'),
    )

    post_data = models.TextField(
        verbose_name=_('POST Data'),
    )

    failures_since_start = models.PositiveIntegerField(
        verbose_name=_('Failed Logins'),
    )

    @property
    def failures(self):
        return self.failures_since_start

    def __str__(self):
        return 'Attempted Access: %s' % self.attempt_time


class AccessLog(CommonAccess):
    logout_time = models.DateTimeField(
        verbose_name=_('Logout Time'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return 'Access Log for %s @ %s' % (self.username, self.attempt_time)
