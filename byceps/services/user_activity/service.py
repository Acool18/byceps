# -*- coding: utf-8 -*-

"""
byceps.services.user_activity.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from itertools import chain

from ..newsletter import service as newsletter_service
from ..terms import service as terms_service
from ..user_avatar import service as avatar_service

from .models import Activity, ActivityType


def get_activities_for_user(user_id):
    activities = list(chain(
        get_avatar_updates_for_user(user_id),
        get_terms_consents_for_user(user_id),
        get_newsletter_subscription_updates_for_user(user_id),
    ))

    _sort_activities(activities)

    return activities


def get_avatar_updates_for_user(user_id):
    """Yield the user's avatar updates as activities."""
    avatars = avatar_service.get_avatars_for_user(user_id)

    for avatar in avatars:
        type_ = ActivityType.avatar_update

        yield Activity(avatar.created_at, type_, avatar)


def get_newsletter_subscription_updates_for_user(user_id):
    """Yield the user's newsletter subscription updates as activities."""
    updates = newsletter_service.get_subscription_updates_for_user(user_id)

    for update in updates:
        type_ = ActivityType.newsletter_subscription_update

        yield Activity(update.expressed_at, type_, update)


def get_terms_consents_for_user(user_id):
    """Yield the user's consents to terms as activities."""
    consents = terms_service.get_consents_by_user(user_id)

    for consent in consents:
        type_ = ActivityType.terms_consent

        yield Activity(consent.expressed_at, type_, consent)


def _sort_activities(activities):
    """Sort activities chronologically backwards, in-place."""
    activities.sort(key=lambda a: a.occured_at, reverse=True)