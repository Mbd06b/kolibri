from __future__ import unicode_literals

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from kolibri.auth.constants import role_kinds
from kolibri.auth.models import FacilityUser
from kolibri.auth.permissions.base import RoleBasedPermissions
from kolibri.auth.permissions.general import IsOwn
from kolibri.content.models import UUIDField


class BaseLogModel(models.Model):

    permissions = (
        IsOwn() |
        RoleBasedPermissions(
            target_field="user",
            can_be_created_by=(role_kinds.ADMIN,),
            can_be_read_by=(role_kinds.ADMIN, role_kinds.COACH),
            can_be_updated_by=(role_kinds.ADMIN,),
            can_be_deleted_by=(role_kinds.ADMIN,),
        )
    )

    user = models.ForeignKey(FacilityUser, blank=True, null=True, db_index=True)

    class Meta:
        abstract = True

class ContentInteractionLog(BaseLogModel):
    """
    This Model provides a record of an interaction with a content item.
    """
    content_id = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, db_index=True)
    channel_id = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, db_index=True)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    completion_timestamp = models.DateTimeField(blank=True, null=True)
    item_session = UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    kind = models.CharField(max_length=200, blank=True)  # indicates how extra_fields should be interpreted
    extra_fields = models.TextField(blank=True)


class ContentSummaryLog(BaseLogModel):
    """
    This Model provides a summary of all interactions of a user with a content item.
    """
    content_id = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, db_index=True)
    last_channel_id = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, db_index=True)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    last_activity_timestamp = models.DateTimeField(blank=True, null=True)
    completion_timestamp = models.DateTimeField(blank=True, null=True)
    progress = models.DecimalField(default=0.0, max_digits=2, decimal_places=1)
    kind = models.CharField(max_length=200, blank=True)  # indicates how extra_fields should be interpreted
    extra_fields = models.TextField(blank=True)


class ContentRatingLog(BaseLogModel):
    """
    This Model provides a record of user feedback on content.
    """
    content_id = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, db_index=True)
    channel_id = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, db_index=True)
    quality = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    ease = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    learning = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(blank=True)


class UserSessionLog(BaseLogModel):
    """
    This Model provides a record of a user session in Kolibri.
    """
    channels = models.TextField(blank=True)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    completion_timestamp = models.DateTimeField(blank=True, null=True)
    pages = models.TextField(blank=True)
