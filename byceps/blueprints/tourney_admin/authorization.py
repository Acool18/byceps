# -*- coding: utf-8 -*-

"""
byceps.blueprints.tourney_admin.authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.util.authorization import create_permission_enum


TourneyCategoryPermission = create_permission_enum('tourney_category', [
    'list',
    'create',
    'update',
])