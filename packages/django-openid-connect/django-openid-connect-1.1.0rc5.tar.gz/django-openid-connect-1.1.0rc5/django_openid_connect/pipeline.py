from django.conf import settings
from django.contrib.auth.models import Group
import logging
from django.db.models.fields import UUIDField
from urnparse import URN8141
import uuid
from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
)


class PerunGroup(Model):
    group = ForeignKey('Group', editable=False, on_delete=CASCADE)
    uuid = UUIDField(editable=False)


logger = logging.getLogger(__name__)


def user_groups(strategy, details, user=None, *args, **kwargs):
    """
        Update user group membership using data from OpenId provider.

        :raises ValueError
    """
    print(f"{kwargs}")
    group_attr = kwargs['response'].get(settings.REMOTE_GROUP_KEY, None)
    if not group_attr:
        return

    internal_group_attr = [URN8141.from_string(g) for g in group_attr] #settings.REMOTE_GROUP_FILTER(group_attr)]
    group_names = []
    # Create valid nonexist groups
    for g in internal_group_attr:
        print(f"{g.specific_string.decoded}  -- {g.specific_string.parts} -- {g.rqf_component.fragment} -- {g.rqf_component.query}")
        parts = g.specific_string.parts
        if "groupAttributes" in parts:
            uuid = uuid.UUID(parts[len(parts)-1])
            last_part = g.rqf_component.query.get("displayName")
            if last_part is None:
                last_part = ""
            else:
                last_part = ":" + last_part
            name = f"{g.rqf_component.fragment}{last_part}"
            group_names.append(name)
            print(f"uuid: {uuid} {name}")
            try:
                group = Group.objects.get_or_create(name=name)
                PerunGroup.objects.create(group=group, uuid=uuid)
            except Exception as e:
                print(f"{e}")
                pass
    if user:
        # Remove user from any extra groups that weren't provided by OpenId
        remote_groups = Group.objects.filter(name__in=group_names)
        extra_groups = user.groups.exclude(name__in=[g.name for g in remote_groups] + settings.PROTECTED_GROUPS)
        # if user is superuser means may have groups assigned for test
        if not user.is_superuser:
            for eg in extra_groups:
                logger.debug('Removing {} from group {}'.format(user.username, eg.name))
                eg.user_set.remove(user)

        # Add user to groups provided by OpenId
        local_groups = user.groups.all()
        new_memberships = remote_groups.exclude(name__in=[g.name for g in local_groups] + settings.PROTECTED_GROUPS)
        for ng in new_memberships:
            logger.debug('Adding {} to group {}'.format(user.username, ng.name))
            user.groups.add(ng.pk)
