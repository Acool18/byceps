# -*- coding: utf-8 -*-

"""
byceps.services.orga.birthday_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from itertools import islice

from ...database import db

from ..user_avatar import service as user_avatar_service
from ..user.models.detail import UserDetail
from ..user.models.user import User

from .models import OrgaFlag


def collect_orgas_with_next_birthdays(*, limit=None):
    """Yield the next birthdays of organizers, sorted by month and day."""
    orgas_with_birthdays = _collect_orgas_with_birthdays()

    sorted_orgas = sort_users_by_next_birthday(orgas_with_birthdays)

    if limit is not None:
        sorted_orgas = islice(sorted_orgas, limit)

    orgas = list(sorted_orgas)

    user_ids = frozenset(user.id for user in orgas)

    avatars_by_user_id = user_avatar_service.get_avatars_for_users(user_ids)

    for user in orgas:
        avatar = avatars_by_user_id.get(user.id)

        yield {
            'id': user.id,
            'screen_name': user.screen_name,
            'detail': user.detail,
            'avatar': avatar,
            'is_orga': False,
        }


def _collect_orgas_with_birthdays():
    """Return all organizers whose birthday is known."""
    return User.query \
        .join(OrgaFlag) \
        .join(UserDetail) \
        .filter(UserDetail.date_of_birth != None) \
        .options(db.joinedload('detail')) \
        .all()


def sort_users_by_next_birthday(users):
    return sorted(users,
                  key=lambda user: (
                    user.detail.days_until_next_birthday,
                    -user.detail.age))