# -*- coding: utf-8 -*-

"""
byceps.blueprints.party_admin.authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.util.authorization import create_permission_enum


PartyPermission = create_permission_enum('party', [
    'list',
    'create',
])