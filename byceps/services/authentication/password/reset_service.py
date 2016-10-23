# -*- coding: utf-8 -*-

"""
byceps.services.authentication.password.reset_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import url_for

from ....database import db

from ...email import service as email_service
from ...verification_token import service as verification_token_service


def prepare_password_reset(user):
    """Create a verification token for password reset and email it to
    the user's address.
    """
    verification_token = verification_token_service \
        .build_for_password_reset(user.id)

    db.session.add(verification_token)
    db.session.commit()

    _send_password_reset_email(user, verification_token)


def _send_password_reset_email(user, verification_token):
    confirmation_url = url_for('authentication.password_reset_form',
                               token=verification_token.token,
                               _external=True)

    subject = '{0.screen_name}, so kannst du ein neues Passwort festlegen' \
        .format(user)
    body = (
        'Hallo {0.screen_name},\n\n'
        'du kannst ein neues Passwort festlegen indem du diese URL abrufst: {1}'
    ).format(user, confirmation_url)
    recipients = [user.email_address]

    email_service.send_email(subject=subject, body=body, recipients=recipients)


def reset_password(verification_token, password):
    """Reset the user's password."""
    user = verification_token.user

    db.session.delete(verification_token)
    db.session.commit()

    update_password_hash(user.id, password)