from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.utils import timezone

from .models import Notification

UserModel = get_user_model()


def notification(
    user,
    actor,
    verb,
    notification_type=Notification.notification_type.default,
    timestamp=timezone.now(),
    action_object=None,
    target=None,
    description=None,
):
    """
    Create notification for user or queryset of user or list of user.

    Notifications are actually actions events, which are categorized by four main components.

    Actor. The object that performed the activity.
    Verb. The verb phrase that identifies the action of the activity.
    Action Object. (Optional) The object linked to the action itself.
    Target. (Optional) The object to which the activity was performed.

    Actor, Action Object and Target are GenericForeignKeys to any arbitrary Django object.
    An action is a description of an action that was performed (Verb) at some instant in time by some Actor on some
    optional Target that results in an Action Object getting created/updated/deleted

    Use '{actor} {verb} {action_object(optional)} on {target(optional)}' as description if description is not provided

    """
    if isinstance(user, (QuerySet, list)) and all(
        isinstance(u, UserModel) for u in user
    ):
        users = user
    elif isinstance(user, UserModel):
        users = [user]
    else:
        raise TypeError("Only UserModel or queryset or list of UserModel is supported")
    for user_obj in users:
        if description is None:
            extra_content = ""
            if action_object:
                extra_content += f" {action_object}"
            if target:
                extra_content += f" on {target}"
            description = f"{actor} {verb}{extra_content}"

        Notification.objects.create(
            recipient=user_obj,
            actor_content_object=actor,
            verb=verb,
            description=description,
            notification_type=notification_type,
            timestamp=timestamp,
            action_object_content_object=action_object,
            target_content_object=target,
        )